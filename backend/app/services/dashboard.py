from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.schemas.dashboard import DashboardSummary, PriorityCounts, StatusCounts


def get_summary(db: Session) -> DashboardSummary:
    """Aggregate all tickets in SQL; do not paginate or load rows into Python."""
    statuses = dict(db.execute(select(Ticket.status, func.count(Ticket.id)).group_by(Ticket.status)).all())
    priorities = dict(db.execute(select(Ticket.priority, func.count(Ticket.id)).group_by(Ticket.priority)).all())
    total = sum(statuses.values())
    return DashboardSummary(
        total=total,
        by_status=StatusCounts(**statuses),
        by_priority=PriorityCounts(**priorities),
    )
