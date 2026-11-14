from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.schemas.ai_triage import AITriageRequest, AITriageResponse
from app.services.ai_triage import suggest_triage

router = APIRouter(prefix="/api/v1/ai", tags=["Triagem assistida"], dependencies=[Depends(get_current_user)])


@router.post("/triage", response_model=AITriageResponse)
def triage(payload: AITriageRequest) -> AITriageResponse:
    return suggest_triage(payload)
