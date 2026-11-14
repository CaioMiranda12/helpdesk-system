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
    result = ai_provider._openai_triage(PAYLOAD, "test-key", "gpt-4.1-mini")
    assert result.provider == "openai"
    assert result.priority.value == "high"


def test_network_error_is_503(monkeypatch):
    def fail(*args, **kwargs): raise URLError("offline")
    monkeypatch.setattr(ai_provider.request, "urlopen", fail)
    with pytest.raises(HTTPException) as exc:
        ai_provider._openai_triage(PAYLOAD, "test-key", "gpt-4.1-mini")
    assert exc.value.status_code == 503


def test_invalid_model_output_is_503(monkeypatch):
    class FakeResponse:
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def read(self, *args): return b'{"choices":[{"message":{"content":"{\"priority\":\"critical\",\"category\":\"software\",\"reason\":\"foo\"}"}}]}'
    monkeypatch.setattr(ai_provider.request, "urlopen", lambda *a, **kw: FakeResponse())
    with pytest.raises(HTTPException) as exc:
        ai_provider._openai_triage(PAYLOAD, "test-key", "gpt-4.1-mini")
    assert exc.value.status_code == 503
