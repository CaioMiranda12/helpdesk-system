from datetime import datetime, timezone
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.models.activity import TicketActivity
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketUpdate, Status, Priority

ALLOWED_TRANSITIONS = {
    "open": {"in_progress"},
    "in_progress": {"resolved"},
    "resolved": {"in_progress"},
}

def get_ticket_or_404(db: Session, ticket_id: UUID) -> Ticket:
    ticket = db.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    return ticket

def create_ticket(db: Session, data: TicketCreate) -> Ticket:
    ticket = Ticket(**data.model_dump(mode="json"))
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

def list_tickets(
    db: Session, limit: int, offset: int,
    search: str | None = None,
    status_filter: Status | None = None,
    priority: Priority | None = None,
) -> list[Ticket]:
    query = select(Ticket)
    if search:
        # Escape SQL LIKE wildcards so the user's query is treated literally.
        escaped = search.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        query = query.where(Ticket.title.ilike(f"%{escaped}%", escape="\\"))
    if status_filter is not None:
        query = query.where(Ticket.status == status_filter.value)
    if priority is not None:
        query = query.where(Ticket.priority == priority.value)
    query = query.order_by(Ticket.created_at.desc(), Ticket.id.desc()).limit(limit).offset(offset)
    return list(db.scalars(query).all())

def update_ticket(db: Session, ticket_id: UUID, data: TicketUpdate) -> Ticket:
    ticket = get_ticket_or_404(db, ticket_id)
    for key, value in data.model_dump(exclude_unset=True, mode="json").items():
        setattr(ticket, key, value)
    ticket.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(ticket)
    return ticket

def assign_ticket(db: Session, ticket_id: UUID, assignee_id: UUID | None, actor_id: UUID | None = None) -> Ticket:
    ticket = get_ticket_or_404(db, ticket_id)
    if assignee_id is not None:
        user = db.get(User, assignee_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Agente não encontrado")
        if user.role != "agent":
            raise HTTPException(status_code=409, detail="Somente agentes podem ser responsáveis")
    previous = ticket.assignee_id
    ticket.assignee_id = assignee_id
    if actor_id is not None and previous != assignee_id:
        db.add(TicketActivity(ticket_id=ticket.id, author_id=actor_id, kind="assignment", old_value=str(previous) if previous else None, new_value=str(assignee_id) if assignee_id else None))
    ticket.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(ticket)
    return ticket


def change_ticket_status(db: Session, ticket_id: UUID, new_status: Status, actor_id: UUID | None = None) -> Ticket:
    ticket = get_ticket_or_404(db, ticket_id)
    if new_status.value not in ALLOWED_TRANSITIONS[ticket.status]:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Transição de status não permitida")
    previous = ticket.status
    ticket.status = new_status.value
    if actor_id is not None:
        db.add(TicketActivity(ticket_id=ticket.id, author_id=actor_id, kind="status", old_value=previous, new_value=new_status.value))
    ticket.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(ticket)
    return ticket
