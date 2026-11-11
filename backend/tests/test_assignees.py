"""Regras de atribuição: permissões, integridade e preservação de chamados."""
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

PAYLOAD = {"title": "Problema de acesso", "description": "Não consigo acessar o sistema.", "priority": "medium"}

@pytest.fixture
def scenario():
    engine = create_engine("sqlite+pysqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    @event.listens_for(engine, "connect")
    def register_functions(connection, _):
        connection.create_function("char_length", 1, len)
        connection.execute("PRAGMA foreign_keys=ON")
    Base.metadata.create_all(engine)
    admin = User(email="admin@example.com", name="Admin", password_hash="unused", role="admin")
    agent = User(email="agent@example.com", name="Agente 1", password_hash="unused", role="agent")
    agent2 = User(email="agent2@example.com", name="Agente 2", password_hash="unused", role="agent")
    with Session(engine) as db:
        db.add_all([admin, agent, agent2]); db.commit()
        for user in (admin, agent, agent2): db.refresh(user)
        admin_id, agent_id, agent2_id = admin.id, agent.id, agent2.id
    current = {"id": admin_id}
    def override_db():
        with Session(engine) as db: yield db
    def override_user():
        with Session(engine) as db: return db.get(User, current["id"])
    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_current_user] = override_user
    try:
        yield TestClient(app), current, admin_id, agent_id, agent2_id
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(engine)
        engine.dispose()

def create(client):
    response = client.post('/api/v1/tickets', json=PAYLOAD)
    assert response.status_code == 201, response.text
    return response.json()['id']

def test_admin_can_assign_reassign_and_clear(scenario):
    client, _, _, agent1, agent2 = scenario
    tid = create(client)
    assert client.get(f'/api/v1/tickets/{tid}').json()['assignee_id'] is None
    for uid in (agent1, agent2):
        response = client.patch(f'/api/v1/tickets/{tid}/assignee', json={'assignee_id': str(uid)})
        assert response.status_code == 200, response.text
        assert response.json()['assignee_id'] == str(uid)
        assert response.json()['assignee']['name'].startswith('Agente')
    cleared = client.patch(f'/api/v1/tickets/{tid}/assignee', json={'assignee_id': None})
    assert cleared.status_code == 200
    assert cleared.json()['assignee'] is None

def test_agent_can_view_but_cannot_assign(scenario):
    client, current, _, agent_id, _ = scenario
    tid = create(client)
    current['id'] = agent_id
    assert client.get(f'/api/v1/tickets/{tid}').status_code == 200
    assert client.patch(f'/api/v1/tickets/{tid}/assignee', json={'assignee_id': str(agent_id)}).status_code == 403
    assert client.get(f'/api/v1/tickets/{tid}').json()['assignee_id'] is None

def test_invalid_assignee_does_not_change_ticket(scenario):
    client, _, admin_id, agent_id, _ = scenario
    tid = create(client)
    assert client.patch(f'/api/v1/tickets/{tid}/assignee', json={'assignee_id': str(agent_id)}).status_code == 200
    assert client.patch(f'/api/v1/tickets/{tid}/assignee', json={'assignee_id': str(admin_id)}).status_code == 409
    assert client.patch(f'/api/v1/tickets/{tid}/assignee', json={'assignee_id': str(uuid4())}).status_code == 404
    assert client.patch(f'/api/v1/tickets/{tid}/assignee', json={'assignee_id': 'abc'}).status_code == 422
    assert client.patch(f'/api/v1/tickets/{tid}/assignee', json={}).status_code == 422
    assert client.get(f'/api/v1/tickets/{tid}').json()['assignee_id'] == str(agent_id)

def test_agent_directory_only_agents_and_requires_login(scenario):
    client, current, _, agent_id, _ = scenario
    response = client.get('/api/v1/agents')
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert all(user['role'] == 'agent' for user in response.json())
    assert all('password_hash' not in user for user in response.json())
    current['id'] = agent_id
    assert client.get('/api/v1/agents').status_code == 200

def test_missing_ticket_returns_404(scenario):
    client, _, _, agent_id, _ = scenario
    response = client.patch(f'/api/v1/tickets/{uuid4()}/assignee', json={'assignee_id': str(agent_id)})
    assert response.status_code == 404
