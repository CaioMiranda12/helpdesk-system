import json
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.api.v1 import ai
from app.core.security import get_current_user
from app.main import app
from app.schemas.ai_reply import AIReplyRequest
from app.services import ai_reply

PAYLOAD = AIReplyRequest(title="Sistema fora do ar", description="Não consigo acessar o sistema desde ontem.")


def test_mock_does_not_need_external_api(monkeypatch):
    monkeypatch.setattr(ai_reply, "get_settings", lambda: SimpleNamespace(ai_provider="mock"))
    result = ai_reply.suggest_reply(PAYLOAD)
    assert result.provider == "mock"
    assert len(result.suggestion) >= 10


def test_groq_sdk_is_mocked(monkeypatch):
    settings = SimpleNamespace(ai_provider="groq", groq_api_key="fake-key", groq_model="openai/gpt-oss-20b")
    monkeypatch.setattr(ai_reply, "get_settings", lambda: settings)
    calls = {}

    class FakeGroq:
        def __init__(self, **kwargs):
            calls["config"] = kwargs
            self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))

        def create(self, **kwargs):
            calls["request"] = kwargs
            return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(
                content=json.dumps({"suggestion": "Olá! Vamos verificar seu acesso e retornar com orientações."})
            ))])

    monkeypatch.setattr(ai_reply, "Groq", FakeGroq)
    result = ai_reply.suggest_reply(PAYLOAD)
    assert result.provider == "groq"
    assert calls["request"]["model"] == "openai/gpt-oss-20b"
    assert calls["config"]["api_key"] == "fake-key"


def test_reply_endpoint_requires_auth():
    with TestClient(app) as client:
        response = client.post("/api/v1/ai/reply-suggestion", json=PAYLOAD.model_dump())
    assert response.status_code == 401


def test_reply_endpoint_with_mock_and_validation(monkeypatch):
    monkeypatch.setattr(ai, "run_reply", lambda payload: ai_reply.AIReplyResponse(
        suggestion="Olá! Estamos analisando seu chamado e retornaremos com orientações.", provider="mock"
    ))
    app.dependency_overrides[get_current_user] = lambda: type("TestUser", (), {"id": "test-user"})()
    try:
        with TestClient(app) as client:
            good = client.post("/api/v1/ai/reply-suggestion", json=PAYLOAD.model_dump())
            bad = client.post("/api/v1/ai/reply-suggestion", json={"title": "  ", "description": "curto"})
        assert good.status_code == 200
        assert good.json()["provider"] == "mock"
        assert bad.status_code == 422
    finally:
        app.dependency_overrides.pop(get_current_user, None)


def test_invalid_provider_response_returns_503(monkeypatch):
    settings = SimpleNamespace(ai_provider="groq", groq_api_key="fake-key", groq_model="test")
    monkeypatch.setattr(ai_reply, "get_settings", lambda: settings)

    class FakeGroq:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(completions=SimpleNamespace(create=lambda **kwargs: SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content='{"suggestion":"x"}'))]
            )))

    monkeypatch.setattr(ai_reply, "Groq", FakeGroq)
    with pytest.raises(Exception) as exc:
        ai_reply.suggest_reply(PAYLOAD)
    assert exc.value.status_code == 503
