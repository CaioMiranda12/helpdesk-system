"""Proteção dos dados enviados à IA: testes sem acesso à rede."""
import json
from types import SimpleNamespace

from app.services.ai_privacy import minimize_for_external_ai
from app.services.ai_provider import _messages
from app.schemas.ai_triage import AITriageRequest
from app.schemas.ai_reply import AIReplyRequest
from app.services import ai_reply, ai_activity_summary


def test_minimization_preserves_useful_context():
    text = "Erro ao entrar: ana@example.com, (85) 99999-1234, CPF 123.456.789-09."
    result = minimize_for_external_ai(text)
    assert "Erro ao entrar" in result
    assert "ana@example.com" not in result
    assert "99999-1234" not in result
    assert "123.456.789-09" not in result
    assert "[EMAIL_REMOVIDO]" in result


def test_removes_common_api_keys_and_bearer_tokens():
    text = "Bearer abc.def.ghi e sk-abcdefghijklmnopqrstuvwxyz123"
    result = minimize_for_external_ai(text)
    assert "abc.def.ghi" not in result
    assert "sk-abcdefghijklmnopqrstuvwxyz123" not in result


def test_triage_payload_is_minimized():
    payload = AITriageRequest(title="Falha no login", description="Contato ana@example.com não consegue entrar")
    sent = json.loads(_messages(payload)[1]["content"])
    assert "ana@example.com" not in sent["description"]
    assert "Falha no login" == sent["title"]


def test_reply_payload_is_minimized(monkeypatch):
    monkeypatch.setattr(ai_reply, "get_settings", lambda: SimpleNamespace(
        ai_provider="groq", groq_api_key="fake", groq_model="test"))
    captured = {}

    class FakeGroq:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))

        def create(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(
                content=json.dumps({"suggestion": "Olá! Vamos analisar sua solicitação com cuidado."})))])

    monkeypatch.setattr(ai_reply, "Groq", FakeGroq)
    ai_reply.suggest_reply(AIReplyRequest(
        title="Falha no login", description="Usuário ana@example.com está sem acesso"))
    assert "ana@example.com" not in captured["messages"][1]["content"]


def test_activity_summary_payload_is_minimized(monkeypatch):
    from uuid import uuid4
    monkeypatch.setattr(ai_activity_summary, "get_settings", lambda: SimpleNamespace(
        ai_provider="groq", groq_api_key="fake", groq_model="test"))
    monkeypatch.setattr(ai_activity_summary, "_events", lambda db, tid: [
        {"kind": "comment", "body": "Contato: ana@example.com. Falha persiste."}
    ])
    captured = {}

    class FakeGroq:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))

        def create(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(
                content=json.dumps({"summary": "O problema permanece em investigação."})))])

    monkeypatch.setattr(ai_activity_summary, "Groq", FakeGroq)
    ai_activity_summary.summarize_activities(object(), uuid4())
    assert "ana@example.com" not in captured["messages"][1]["content"]
