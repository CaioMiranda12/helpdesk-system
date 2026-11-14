import pytest
from pydantic import ValidationError

from app.schemas.ai_triage import (
    TriageRequest,
    TriageSuggestion,
)


def test_triage_request_accepts_valid_data():
    request = TriageRequest(
        title="Impressora sem papel",
        description="Não consigo imprimir documentos.",
    )

    assert request.title == "Impressora sem papel"


def test_triage_request_rejects_short_title():
    with pytest.raises(ValidationError):
        TriageRequest(
            title="Erro",
            description="Descrição suficientemente longa.",
        )


def test_triage_suggestion_accepts_valid_response():
    suggestion = TriageSuggestion(
        category="hardware",
        priority="high",
        reason="Equipamento indisponível.",
    )

    assert suggestion.priority == "high"


def test_triage_suggestion_rejects_invalid_priority():
    with pytest.raises(ValidationError):
        TriageSuggestion(
            category="hardware",
            priority="critical",
            reason="Prioridade não permitida.",
        )