"""Índice para consultar histórico por chamado e ordem cronológica.

Revision ID: 0005_index_ticket_activities
Revises: 0004_create_ticket_activities
"""
from alembic import op

revision = "0005_index_ticket_activities"
down_revision = "0004_create_ticket_activities"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        "ix_ticket_activities_ticket_created_id",
        "ticket_activities",
        ["ticket_id", "created_at", "id"],
    )


def downgrade():
    op.drop_index("ix_ticket_activities_ticket_created_id", table_name="ticket_activities")
