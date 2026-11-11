"""create tickets table

Revision ID: 0001_create_tickets
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_create_tickets"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tickets",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("title", sa.String(120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("priority", sa.String(10), server_default="medium", nullable=False),
        sa.Column("status", sa.String(20), server_default="open", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("priority IN ('low', 'medium', 'high')", name="ck_tickets_priority"),
        sa.CheckConstraint("status IN ('open', 'in_progress', 'resolved')", name="ck_tickets_status"),
        sa.CheckConstraint("char_length(trim(title)) BETWEEN 5 AND 120", name="ck_tickets_title_length"),
        sa.CheckConstraint("char_length(trim(description)) BETWEEN 10 AND 2000", name="ck_tickets_description_length"),
    )


def downgrade() -> None:
    op.drop_table("tickets")
