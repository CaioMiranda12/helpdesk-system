from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.rate_limit import limit_ai
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.activity import ActivityRead, CommentCreate
from app.schemas.ai_activity_summary import AIActivitySummaryResponse
from app.services.ai_activity_summary import summarize_activities
from app.services import activities as service

router = APIRouter(prefix="/api/v1/tickets", tags=["Atividades"], dependencies=[Depends(get_current_user)])

@router.get("/{ticket_id}/activities", response_model=list[ActivityRead])
def list_activities(ticket_id: UUID, limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    return service.list_activities(db, ticket_id, limit, offset)

@router.post("/{ticket_id}/comments", response_model=ActivityRead, status_code=status.HTTP_201_CREATED)
def create_comment(ticket_id: UUID, payload: CommentCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return service.create_comment(db, ticket_id, user.id, payload.body)


@router.post("/{ticket_id}/activities/ai-summary", response_model=AIActivitySummaryResponse)
def ai_activity_summary(ticket_id: UUID, db: Session = Depends(get_db), _limit: None = Depends(limit_ai)) -> AIActivitySummaryResponse:
    return summarize_activities(db, ticket_id)
