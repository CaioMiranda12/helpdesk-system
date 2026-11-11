from app.core.security import get_current_user
from app.models.user import User
import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.ticket import Ticket  # noqa: F401: registra o modelo no metadata

@pytest.fixture
def client():
    engine = create_engine("sqlite+pysqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    @event.listens_for(engine, "connect")
    def register_functions(connection, _):
        connection.create_function("char_length", 1, len)
    Base.metadata.create_all(engine)
    def override_db():
        with Session(engine) as session:
            yield session
    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_current_user] = lambda: User(email="tester@example.com", name="Tester", role="admin", password_hash="unused")
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(engine)
        engine.dispose()

PAYLOAD = {"title": "Erro no relatório", "description": "O relatório não carrega na tela.", "priority": "high"}

def test_create_list_get_and_update(client):
    response = client.post("/api/v1/tickets", json=PAYLOAD)
    assert response.status_code == 201, response.text
    ticket = response.json()
    assert ticket["status"] == "open"
    assert ticket["priority"] == "high"
    ticket_id = ticket["id"]
    assert client.get(f"/api/v1/tickets/{ticket_id}").status_code == 200
    listing = client.get("/api/v1/tickets?limit=1&offset=0")
    assert listing.status_code == 200
    assert len(listing.json()) == 1
    edited = client.patch(f"/api/v1/tickets/{ticket_id}", json={"title": "Relatório indisponível"})
    assert edited.status_code == 200, edited.text
    assert edited.json()["title"] == "Relatório indisponível"

def test_status_transition_rules(client):
    ticket_id = client.post("/api/v1/tickets", json=PAYLOAD).json()["id"]
    url = f"/api/v1/tickets/{ticket_id}/status"
    assert client.patch(url, json={"status": "resolved"}).status_code == 409
    assert client.patch(url, json={"status": "in_progress"}).status_code == 200
    assert client.patch(url, json={"status": "resolved"}).status_code == 200
    assert client.patch(url, json={"status": "in_progress"}).status_code == 200

def test_validation_and_not_found(client):
    assert client.post("/api/v1/tickets", json={"title": "oi", "description": "curta"}).status_code == 422
    assert client.get(f"/api/v1/tickets/{uuid.uuid4()}").status_code == 404
    assert client.get("/api/v1/tickets?limit=101").status_code == 422
    assert client.patch(f"/api/v1/tickets/{uuid.uuid4()}", json={"title": "Título válido"}).status_code == 404
    ticket_id = client.post("/api/v1/tickets", json=PAYLOAD).json()["id"]
    assert client.patch(f"/api/v1/tickets/{ticket_id}", json={}).status_code == 422
    assert client.patch(f"/api/v1/tickets/{ticket_id}", json={"priority": None}).status_code == 422


def test_pagination_does_not_repeat_records(client):
    ids = [client.post("/api/v1/tickets", json={**PAYLOAD, "title": f"Chamado número {i}"}).json()["id"] for i in range(3)]
    first = client.get("/api/v1/tickets?limit=2&offset=0")
    second = client.get("/api/v1/tickets?limit=2&offset=2")
    assert first.status_code == second.status_code == 200
    received = [ticket["id"] for ticket in first.json() + second.json()]
    assert len(received) == 3
    assert set(received) == set(ids)

def test_invalid_inputs_do_not_create_or_modify_ticket(client):
    assert client.post("/api/v1/tickets", json={**PAYLOAD, "title": "    "}).status_code == 422
    assert client.post("/api/v1/tickets", json={**PAYLOAD, "priority": "urgent"}).status_code == 422
    created = client.post("/api/v1/tickets", json=PAYLOAD).json()
    ticket_id = created["id"]
    assert client.patch(f"/api/v1/tickets/{ticket_id}", json={"description": "    "}).status_code == 422
    assert client.get(f"/api/v1/tickets/{ticket_id}").json()["description"] == PAYLOAD["description"]
    assert client.patch(f"/api/v1/tickets/{ticket_id}/status", json={"status": "invalid"}).status_code == 422
    assert client.get(f"/api/v1/tickets/{ticket_id}").json()["status"] == "open"

def test_invalid_status_transition_does_not_persist(client):
    ticket_id = client.post("/api/v1/tickets", json=PAYLOAD).json()["id"]
    url = f"/api/v1/tickets/{ticket_id}/status"
    assert client.patch(url, json={"status": "resolved"}).status_code == 409
    assert client.get(f"/api/v1/tickets/{ticket_id}").json()["status"] == "open"

def test_invalid_pagination_and_uuid(client):
    assert client.get("/api/v1/tickets?offset=-1").status_code == 422
    assert client.get("/api/v1/tickets?limit=0").status_code == 422
    assert client.get("/api/v1/tickets/not-a-uuid").status_code == 422
