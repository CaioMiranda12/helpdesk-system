"""Regressão de comentários e histórico, sem PostgreSQL local."""
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from app.core.security import get_current_user
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.user import User

@pytest.fixture
def scenario():
    engine = create_engine("sqlite+pysqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    @event.listens_for(engine, "connect")
    def sqlite_functions(connection, _):
        connection.create_function("char_length", 1, len)
        connection.execute("PRAGMA foreign_keys=ON")
    Base.metadata.create_all(engine)
    admin = User(email="admin11@example.com", name="Admin", password_hash="unused", role="admin")
    agent = User(email="agent11@example.com", name="Agente", password_hash="unused", role="agent")
    with Session(engine) as db:
        db.add_all([admin, agent]); db.commit(); db.refresh(admin); db.refresh(agent)
        ids = {"admin": admin.id, "agent": agent.id}
    current = {"id": ids["admin"]}
    def override_db():
        with Session(engine) as db: yield db
    def override_user():
        with Session(engine) as db: return db.get(User, current["id"])
    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_current_user] = override_user
    try: yield TestClient(app), current, ids
    finally:
        app.dependency_overrides.clear(); Base.metadata.drop_all(engine); engine.dispose()

def new_ticket(client):
    response = client.post("/api/v1/tickets", json={"title":"Chamado de teste", "description":"Descrição para testar atividades."})
    assert response.status_code == 201, response.text
    return response.json()["id"]

def test_comment_is_saved_with_author(scenario):
    client, current, ids = scenario
    tid = new_ticket(client)
    current["id"] = ids["agent"]
    response = client.post(f"/api/v1/tickets/{tid}/comments", json={"body":"  Investigando o problema.  "})
    assert response.status_code == 201, response.text
    assert response.json()["body"] == "Investigando o problema."
    assert response.json()["author"]["name"] == "Agente"
    events = client.get(f"/api/v1/tickets/{tid}/activities").json()
    assert len(events) == 1 and events[0]["kind"] == "comment"

def test_status_and_assignment_are_recorded(scenario):
    client, _, ids = scenario
    tid = new_ticket(client)
    assert client.patch(f"/api/v1/tickets/{tid}/status", json={"status":"in_progress"}).status_code == 200
    assert client.patch(f"/api/v1/tickets/{tid}/assignee", json={"assignee_id":str(ids["agent"])}).status_code == 200
    events = client.get(f"/api/v1/tickets/{tid}/activities").json()
    assert {event["kind"] for event in events} == {"status", "assignment"}
    assert next(event for event in events if event["kind"] == "status")["old_value"] == "open"

def test_invalid_comment_and_transition_do_not_generate_events(scenario):
    client, _, _ = scenario
    tid = new_ticket(client)
    for body in ("", "   ", "a" * 2001):
        assert client.post(f"/api/v1/tickets/{tid}/comments", json={"body":body}).status_code == 422
    assert client.patch(f"/api/v1/tickets/{tid}/status", json={"status":"resolved"}).status_code == 409
    assert client.get(f"/api/v1/tickets/{tid}/activities").json() == []

def test_missing_ticket_and_pagination(scenario):
    client, _, _ = scenario
    missing = uuid4()
    assert client.get(f"/api/v1/tickets/{missing}/activities").status_code == 404
    assert client.post(f"/api/v1/tickets/{missing}/comments", json={"body":"Comentário válido"}).status_code == 404
    tid = new_ticket(client)
    for i in range(3):
        assert client.post(f"/api/v1/tickets/{tid}/comments", json={"body":f"Mensagem {i}"}).status_code == 201
    assert len(client.get(f"/api/v1/tickets/{tid}/activities?limit=2&offset=1").json()) == 2
    assert client.get(f"/api/v1/tickets/{tid}/activities?limit=101").status_code == 422
