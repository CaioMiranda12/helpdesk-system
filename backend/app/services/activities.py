from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.models.activity import TicketActivity
from app.services.tickets import get_ticket_or_404


def list_activities(db: Session, ticket_id: UUID, limit: int = 50, offset: int = 0) -> list[TicketActivity]:
    get_ticket_or_404(db, ticket_id)
    query = (select(TicketActivity).options(joinedload(TicketActivity.author))
             .where(TicketActivity.ticket_id == ticket_id)
             .order_by(TicketActivity.created_at.desc(), TicketActivity.id.desc())
             .limit(limit).offset(offset))
    return list(db.scalars(query).all())


def create_comment(db: Session, ticket_id: UUID, author_id: UUID, body: str) -> TicketActivity:
    get_ticket_or_404(db, ticket_id)
    activity = TicketActivity(ticket_id=ticket_id, author_id=author_id, kind="comment", body=body)
    db.add(activity)
    db.commit()
    return db.scalar(select(TicketActivity).options(joinedload(TicketActivity.author)).where(TicketActivity.id == activity.id))
