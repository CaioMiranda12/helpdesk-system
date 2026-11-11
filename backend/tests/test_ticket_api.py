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
