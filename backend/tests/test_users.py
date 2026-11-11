from fastapi.testclient import TestClient
from test_auth import auth_client, token  # noqa: F401


def headers(client: TestClient, email: str, password: str):
    access_token = token(client, email, password).json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


def test_admin_lists_users_without_password_hash(auth_client):
    response = auth_client.get("/api/v1/users", headers=headers(auth_client, "admin@example.com", "strong-password-123"))
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert all("password_hash" not in user and "password" not in user for user in response.json())


def test_agent_cannot_list_users(auth_client):
    response = auth_client.get("/api/v1/users", headers=headers(auth_client, "agent@example.com", "strong-password-456"))
    assert response.status_code == 403


def test_anonymous_cannot_list_users(auth_client):
    assert auth_client.get("/api/v1/users").status_code == 401


def test_admin_creates_and_lists_new_user(auth_client):
    auth = headers(auth_client, "admin@example.com", "strong-password-123")
    created = auth_client.post("/api/v1/users", headers=auth, json={"name": "Nova Agente", "email": "nova@example.com", "password": "senha-super-segura", "role": "agent"})
    assert created.status_code == 201
    users = auth_client.get("/api/v1/users", headers=auth).json()
    assert any(u["email"] == "nova@example.com" for u in users)


def test_list_users_invalid_pagination(auth_client):
    auth = headers(auth_client, "admin@example.com", "strong-password-123")
    assert auth_client.get("/api/v1/users?limit=0", headers=auth).status_code == 422
    assert auth_client.get("/api/v1/users?offset=-1", headers=auth).status_code == 422
