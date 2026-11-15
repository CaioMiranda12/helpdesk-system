import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from app.core.rate_limit import limiter
from app.core.security import hash_password
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models import User


@pytest.fixture
def auth_client():
    limiter.clear()
    engine = create_engine("sqlite+pysqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    @event.listens_for(engine, "connect")
    def functions(conn, _):
        conn.create_function("char_length", 1, len)
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        db.add_all([
            User(email="admin@example.com", name="Admin", password_hash=hash_password("strong-password-123"), role="admin"),
            User(email="agent@example.com", name="Agent", password_hash=hash_password("strong-password-456"), role="agent"),
        ])
        db.commit()
    def override_db():
        with Session(engine) as db:
            yield db
    app.dependency_overrides[get_db] = override_db
    try:
        yield TestClient(app)
    finally:
        limiter.clear()
        app.dependency_overrides.clear()
        Base.metadata.drop_all(engine)
        engine.dispose()


def token(client, email, password):
    return client.post("/api/v1/auth/login", json={"email": email, "password": password})


def test_login_and_me(auth_client):
    response = token(auth_client, "admin@example.com", "strong-password-123")
    assert response.status_code == 200
    assert response.json()["user"]["role"] == "admin"
    assert auth_client.get("/api/v1/auth/me", headers={"Authorization": "Bearer " + response.json()["access_token"]}).status_code == 200


def test_invalid_login_and_protected_routes(auth_client):
    assert token(auth_client, "admin@example.com", "wrong-password").status_code == 401
    assert auth_client.get("/api/v1/tickets").status_code == 401
    assert auth_client.get("/api/v1/dashboard/summary").status_code == 401
    assert auth_client.get("/api/v1/tickets", headers={"Authorization": "Bearer invalid"}).status_code == 401
    assert auth_client.get("/health").status_code == 200


def test_agent_cannot_create_users(auth_client):
    t = token(auth_client, "agent@example.com", "strong-password-456").json()["access_token"]
    headers = {"Authorization": "Bearer " + t}
    assert auth_client.get("/api/v1/tickets", headers=headers).status_code == 200
    response = auth_client.post("/api/v1/users", headers=headers, json={"email": "new@example.com", "name": "New User", "password": "new-strong-password"})
    assert response.status_code == 403


def test_admin_creates_user_and_prevents_duplicate(auth_client):
    t = token(auth_client, "admin@example.com", "strong-password-123").json()["access_token"]
    headers = {"Authorization": "Bearer " + t}
    payload = {"email": "NEW@example.com", "name": "New User", "password": "new-strong-password"}
    created = auth_client.post("/api/v1/users", headers=headers, json=payload)
    assert created.status_code == 201, created.text
    assert created.json()["email"] == "new@example.com"
    assert "password_hash" not in created.json()
    assert auth_client.post("/api/v1/users", headers=headers, json=payload).status_code == 409
    assert token(auth_client, "new@example.com", "new-strong-password").status_code == 200


def test_short_password_rejected(auth_client):
    t = token(auth_client, "admin@example.com", "strong-password-123").json()["access_token"]
    response = auth_client.post("/api/v1/users", headers={"Authorization": "Bearer " + t}, json={"email": "short@example.com", "name": "Short", "password": "123"})
    assert response.status_code == 422
