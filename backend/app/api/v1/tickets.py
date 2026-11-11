from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.ticket import TicketCreate, TicketRead, TicketUpdate, TicketStatusUpdate, TicketAssigneeUpdate, Status, Priority
from app.services import tickets as service

from app.core.security import get_current_user, require_admin
from app.models.user import User

router = APIRouter(dependencies=[Depends(get_current_user)], prefix="/api/v1/tickets", tags=["Tickets"])

@router.post("", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    return service.create_ticket(db, payload)

@router.get("", response_model=list[TicketRead])
def list_tickets(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    search: str | None = Query(default=None, max_length=120),
    status_filter: Status | None = Query(default=None, alias="status"),
    priority: Priority | None = Query(default=None),
    db: Session = Depends(get_db),
):
    normalized_search = search.strip() if search is not None else None
    return service.list_tickets(db, limit, offset, normalized_search, status_filter, priority)

@router.get("/{ticket_id}", response_model=TicketRead)
def get_ticket(ticket_id: UUID, db: Session = Depends(get_db)):
    return service.get_ticket_or_404(db, ticket_id)

@router.patch("/{ticket_id}", response_model=TicketRead)
def update_ticket(ticket_id: UUID, payload: TicketUpdate, db: Session = Depends(get_db)):
    return service.update_ticket(db, ticket_id, payload)

@router.patch("/{ticket_id}/status", response_model=TicketRead)
def update_status(ticket_id: UUID, payload: TicketStatusUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return service.change_ticket_status(db, ticket_id, payload.status, user.id)

@router.patch("/{ticket_id}/assignee", response_model=TicketRead)
def update_assignee(
    ticket_id: UUID,
    payload: TicketAssigneeUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    return service.assign_ticket(db, ticket_id, payload.assignee_id, _admin.id)
