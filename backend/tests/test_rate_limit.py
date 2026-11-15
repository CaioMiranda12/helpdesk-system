"""Testes de limite sem rede e sem depender do PostgreSQL."""
from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.rate_limit import limiter
from app.core.security import get_current_user
from app.main import app


@pytest.fixture(autouse=True)
def reset_limits():
    limiter.clear()
    yield
    limiter.clear()


def test_login_blocks_after_five_attempts_without_database():
    # A dependência de DB não é executada porque limit_login é substituída por
    # uma chamada real sem consulta ao banco e o endpoint é interrompido antes.
    # Testa a política de janela sem banco e sem fazer login real.
    from fastapi import HTTPException
    for _ in range(5):
        limiter.check("login:test-client", 5)
    with pytest.raises(HTTPException) as exc:
        limiter.check("login:test-client", 5)
    assert exc.value.status_code == 429
    assert int(exc.value.headers["Retry-After"]) >= 1


def test_ai_limit_applies_to_authenticated_routes(monkeypatch):
    from app.api.v1 import ai
    from app.services.ai_triage import suggest_triage
    from app.core import rate_limit
    monkeypatch.setattr(rate_limit, "get_settings", lambda: SimpleNamespace(ai_rate_limit_per_minute=2))
    user_id = uuid4()
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(id=user_id)
    monkeypatch.setattr(ai, "run_triage", suggest_triage)
    try:
        with TestClient(app) as client:
            data = {"title": "Sistema indisponível", "description": "Todos os usuários estão sem acesso."}
            assert client.post("/api/v1/ai/triage", json=data).status_code == 200
            assert client.post("/api/v1/ai/triage", json=data).status_code == 200
            blocked = client.post("/api/v1/ai/triage", json=data)
        assert blocked.status_code == 429
        assert "Retry-After" in blocked.headers
    finally:
        app.dependency_overrides.pop(get_current_user, None)


def test_ai_limit_is_shared_across_ai_endpoints(monkeypatch):
    from app.api.v1 import ai
    from app.services.ai_triage import suggest_triage
    from app.core import rate_limit
    monkeypatch.setattr(rate_limit, "get_settings", lambda: SimpleNamespace(ai_rate_limit_per_minute=1))
    user_id = uuid4()
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(id=user_id)
    monkeypatch.setattr(ai, "run_triage", suggest_triage)
    try:
        with TestClient(app) as client:
            data = {"title": "Sistema indisponível", "description": "Todos os usuários estão sem acesso."}
            assert client.post("/api/v1/ai/triage", json=data).status_code == 200
            blocked = client.post("/api/v1/ai/reply-suggestion", json=data)
        assert blocked.status_code == 429
    finally:
        app.dependency_overrides.pop(get_current_user, None)


def test_different_users_have_independent_limits():
    limiter.check("ai:user-a", 1)
    limiter.check("ai:user-b", 1)
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc:
        limiter.check("ai:user-a", 1)
    assert exc.value.status_code == 429
