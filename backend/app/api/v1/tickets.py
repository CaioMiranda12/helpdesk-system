from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.ticket import TicketCreate, TicketRead, TicketUpdate, TicketStatusUpdate
from app.services import tickets as service

router = APIRouter(prefix="/api/v1/tickets", tags=["Tickets"])

@router.post("", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    return service.create_ticket(db, payload)

@router.get("", response_model=list[TicketRead])
def list_tickets(limit: int = Query(default=20, ge=1, le=100), offset: int = Query(default=0, ge=0), db: Session = Depends(get_db)):
    return service.list_tickets(db, limit, offset)

@router.get("/{ticket_id}", response_model=TicketRead)
def get_ticket(ticket_id: UUID, db: Session = Depends(get_db)):
    return service.get_ticket_or_404(db, ticket_id)

@router.patch("/{ticket_id}", response_model=TicketRead)
def update_ticket(ticket_id: UUID, payload: TicketUpdate, db: Session = Depends(get_db)):
    return service.update_ticket(db, ticket_id, payload)

@router.patch("/{ticket_id}/status", response_model=TicketRead)
def update_status(ticket_id: UUID, payload: TicketStatusUpdate, db: Session = Depends(get_db)):
    return service.change_ticket_status(db, ticket_id, payload.status)
