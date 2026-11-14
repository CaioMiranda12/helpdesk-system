from fastapi.testclient import TestClient
from app.core.security import get_current_user
from app.main import app
from app.schemas.ai_triage import AITriageRequest
from app.services.ai_triage import suggest_triage


def test_mock_triage_high_priority_and_software_category():
    result = suggest_triage(AITriageRequest(
        title="Sistema financeiro fora do ar",
        description="Ninguém consegue emitir nota fiscal desde cedo.",
    ))
    assert result.priority.value == "high"
    assert result.category.value == "software"
    assert result.provider == "mock"


def test_mock_triage_is_deterministic():
    payload = AITriageRequest(title="Solicitar melhoria", description="Gostaria de um novo relatório mensal.")
    assert suggest_triage(payload) == suggest_triage(payload)
    assert suggest_triage(payload).priority.value == "low"


def test_triage_requires_authentication():
    with TestClient(app) as client:
        response = client.post("/api/v1/ai/triage", json={
            "title": "Sistema fora do ar", "description": "Todos os usuários foram afetados.",
        })
    assert response.status_code == 401


def test_triage_endpoint_authenticated_without_database():
    app.dependency_overrides[get_current_user] = lambda: object()
    try:
        with TestClient(app) as client:
            response = client.post("/api/v1/ai/triage", json={
                "title": "Sistema fora do ar", "description": "Todos os usuários foram afetados.",
            })
            invalid = client.post("/api/v1/ai/triage", json={
                "title": "    ", "description": "curto",
            })
        assert response.status_code == 200, response.text
        assert response.json()["priority"] == "high"
        assert invalid.status_code == 422
    finally:
        app.dependency_overrides.pop(get_current_user, None)
