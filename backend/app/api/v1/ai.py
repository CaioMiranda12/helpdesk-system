from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.schemas.ai_triage import AITriageRequest, AITriageResponse
from app.schemas.ai_reply import AIReplyRequest, AIReplyResponse
from app.services.ai_provider import triage as run_triage
from app.services.ai_reply import suggest_reply as run_reply

router = APIRouter(prefix="/api/v1/ai", tags=["Assistência com IA"], dependencies=[Depends(get_current_user)])


@router.post("/triage", response_model=AITriageResponse)
def triage(payload: AITriageRequest) -> AITriageResponse:
    return run_triage(payload)


@router.post("/reply-suggestion", response_model=AIReplyResponse)
def reply_suggestion(payload: AIReplyRequest) -> AIReplyResponse:
    return run_reply(payload)
