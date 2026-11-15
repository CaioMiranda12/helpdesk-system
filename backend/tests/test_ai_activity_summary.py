"""Testes isolados: nenhuma chamada externa nem PostgreSQL necessário."""
import json
from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException

from app.api.v1 import activities
from app.core.security import get_current_user
from app.db.session import get_db
from app.main import app
from app.services import ai_activity_summary as service

TICKET_ID = uuid4()
EVENTS = [{"kind": "comment", "body": "Investigando falha."},
          {"kind": "status", "from": "open", "to": "in_progress"}]


def test_mock_summary(monkeypatch):
    monkeypatch.setattr(service, "_events", lambda db, tid: EVENTS)
    monkeypatch.setattr(service, "get_settings", lambda: SimpleNamespace(ai_provider="mock"))
    result = service.summarize_activities(object(), TICKET_ID)
    assert result.provider == "mock"
    assert result.activities_considered == 2
    assert "2 atividade" in result.summary


def test_no_activities_returns_409(monkeypatch):
    monkeypatch.setattr(service, "_events", lambda db, tid: [])
    with pytest.raises(HTTPException) as exc:
        service.summarize_activities(object(), TICKET_ID)
    assert exc.value.status_code == 409


def test_groq_sdk_mock_and_safe_payload(monkeypatch):
    monkeypatch.setattr(service, "_events", lambda db, tid: EVENTS)
    monkeypatch.setattr(service, "get_settings", lambda: SimpleNamespace(
        ai_provider="groq", groq_api_key="fake", groq_model="openai/gpt-oss-20b"))
    calls = {}

    class FakeGroq:
        def __init__(self, **kwargs):
            calls["config"] = kwargs
            self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))

        def create(self, **kwargs):
            calls["request"] = kwargs
            return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(
                content=json.dumps({"summary": "O atendimento foi iniciado e está em andamento."})
            ))])

    monkeypatch.setattr(service, "Groq", FakeGroq)
    result = service.summarize_activities(object(), TICKET_ID)
    assert result.provider == "groq"
    assert result.activities_considered == 2
    assert calls["request"]["model"] == "openai/gpt-oss-20b"
    assert "Investigando falha" in calls["request"]["messages"][1]["content"]
    assert calls["config"]["api_key"] == "fake"


def test_invalid_provider_response_is_503(monkeypatch):
    monkeypatch.setattr(service, "_events", lambda db, tid: EVENTS)
    monkeypatch.setattr(service, "get_settings", lambda: SimpleNamespace(
        ai_provider="groq", groq_api_key="fake", groq_model="test"))

    class FakeGroq:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(completions=SimpleNamespace(create=lambda **kwargs: SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content='{"summary":"x"}'))]
            )))

    monkeypatch.setattr(service, "Groq", FakeGroq)
    with pytest.raises(HTTPException) as exc:
        service.summarize_activities(object(), TICKET_ID)
    assert exc.value.status_code == 503


def test_endpoint_requires_auth():
    with TestClient(app) as client:
        response = client.post(f"/api/v1/tickets/{TICKET_ID}/activities/ai-summary")
    assert response.status_code == 401


def test_endpoint_authenticated(monkeypatch):
    monkeypatch.setattr(activities, "summarize_activities", lambda db, tid: {
        "summary": "O atendimento foi iniciado e está em andamento.",
        "provider": "mock", "activities_considered": 2,
    })
    app.dependency_overrides[get_current_user] = lambda: object()
    app.dependency_overrides[get_db] = lambda: object()
    try:
        with TestClient(app) as client:
            response = client.post(f"/api/v1/tickets/{TICKET_ID}/activities/ai-summary")
        assert response.status_code == 200, response.text
        assert response.json()["activities_considered"] == 2
    finally:
        app.dependency_overrides.pop(get_current_user, None)
        app.dependency_overrides.pop(get_db, None)
