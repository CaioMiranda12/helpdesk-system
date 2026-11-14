import json
from urllib.error import URLError
import pytest
from fastapi import HTTPException
from app.core.config import Settings
from app.schemas.ai_triage import AITriageRequest
from app.services import ai_provider

PAYLOAD = AITriageRequest(title="Sistema fora do ar", description="Ninguém consegue trabalhar hoje.")


def test_mock_is_default(monkeypatch):
    monkeypatch.setattr(ai_provider, "get_settings", lambda: type("S", (), {"ai_provider": "mock"})())
    result = ai_provider.triage(PAYLOAD)
    assert result.provider == "mock"
    assert result.priority.value == "high"


def test_missing_key_is_safe(monkeypatch):
    monkeypatch.setattr(ai_provider, "get_settings", lambda: type("S", (), {"ai_provider": "openai", "openai_api_key": "", "openai_model": "gpt-4.1-mini"})())
    with pytest.raises(HTTPException) as exc:
        ai_provider.triage(PAYLOAD)
    assert exc.value.status_code == 503


def test_openai_response_is_validated(monkeypatch):
    class FakeResponse:
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def read(self, *args): return json.dumps({"choices": [{"message": {"content": json.dumps({"priority": "high", "category": "software", "reason": "Serviço indisponível"})}}]}).encode()
    def fake_urlopen(req, timeout):
        assert timeout == 12
        assert req.full_url == "https://api.openai.com/v1/chat/completions"
        return FakeResponse()
    monkeypatch.setattr(ai_provider.request, "urlopen", fake_urlopen)
    result = ai_provider._remote_triage(PAYLOAD, "test-key", "gpt-4.1-mini", "openai")
    assert result.provider == "openai"
    assert result.priority.value == "high"


def test_network_error_is_503(monkeypatch):
    def fail(*args, **kwargs): raise URLError("offline")
    monkeypatch.setattr(ai_provider.request, "urlopen", fail)
    with pytest.raises(HTTPException) as exc:
        ai_provider._remote_triage(PAYLOAD, "test-key", "gpt-4.1-mini", "openai")
    assert exc.value.status_code == 503


def test_invalid_model_output_is_503(monkeypatch):
    class FakeResponse:
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def read(self, *args): return b'{"choices":[{"message":{"content":"{\"priority\":\"critical\",\"category\":\"software\",\"reason\":\"foo\"}"}}]}'
    monkeypatch.setattr(ai_provider.request, "urlopen", lambda *a, **kw: FakeResponse())
    with pytest.raises(HTTPException) as exc:
        ai_provider._remote_triage(PAYLOAD, "test-key", "gpt-4.1-mini", "openai")
    assert exc.value.status_code == 503



def test_groq_uses_correct_endpoint_and_model(monkeypatch):
    from types import SimpleNamespace

    calls = {}

    class FakeCompletions:
        def create(self, **kwargs):
            calls["request"] = kwargs

            content = json.dumps({
                "priority": "high",
                "category": "software",
                "reason": "Sistema indisponível",
            })

            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        message=SimpleNamespace(content=content)
                    )
                ]
            )

    class FakeGroq:
        def __init__(self, api_key, timeout, max_retries):
            calls["api_key"] = api_key
            calls["timeout"] = timeout
            calls["max_retries"] = max_retries
            self.chat = SimpleNamespace(
                completions=FakeCompletions()
            )

    monkeypatch.setattr(ai_provider, "Groq", FakeGroq)

    result = ai_provider._remote_triage(
        PAYLOAD,
        "test-groq-key",
        "openai/gpt-oss-20b",
        "groq",
    )

    assert calls["api_key"] == "test-groq-key"
    assert calls["timeout"] == 12.0
    assert calls["max_retries"] == 0

    assert calls["request"]["model"] == "openai/gpt-oss-20b"
    assert calls["request"]["temperature"] == 0
    assert calls["request"]["response_format"] == {
        "type": "json_object"
    }

    assert result.priority == "high"
    assert result.category == "software"
    assert result.provider == "groq"


def test_groq_selection(monkeypatch):
    settings = type("S", (), {"ai_provider": "groq", "groq_api_key": "", "groq_model": "openai/gpt-oss-20b"})()
    monkeypatch.setattr(ai_provider, "get_settings", lambda: settings)
    with pytest.raises(HTTPException) as exc:
        ai_provider.triage(PAYLOAD)
    assert exc.value.status_code == 503
