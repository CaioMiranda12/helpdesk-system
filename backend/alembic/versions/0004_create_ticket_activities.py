"""Comentários e histórico de chamados.

Revision ID: 0004_create_ticket_activities
Revises: 0003_add_ticket_assignee
"""
from alembic import op
import sqlalchemy as sa

revision = "0004_create_ticket_activities"
down_revision = "0003_add_ticket_assignee"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "ticket_activities",
        sa.Column("id", sa.Uuid(), primary_key=True, nullable=False),
        sa.Column("ticket_id", sa.Uuid(), sa.ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False),
        sa.Column("author_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("kind", sa.String(20), nullable=False),
        sa.Column("body", sa.Text(), nullable=True),
        sa.Column("old_value", sa.String(255), nullable=True),
        sa.Column("new_value", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("kind IN ('comment', 'status', 'assignment')", name="ck_ticket_activities_kind"),
    )
    op.create_index("ix_ticket_activities_ticket_id", "ticket_activities", ["ticket_id"])


def downgrade():
    op.drop_index("ix_ticket_activities_ticket_id", table_name="ticket_activities")
    op.drop_table("ticket_activities")
