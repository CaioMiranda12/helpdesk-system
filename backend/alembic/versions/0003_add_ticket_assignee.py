"""Adiciona responsável opcional aos chamados.

Revision ID: 0003_add_ticket_assignee
Revises: 0002_create_users
"""
from alembic import op
import sqlalchemy as sa

revision = "0003_add_ticket_assignee"
down_revision = "0002_create_users"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("tickets", sa.Column("assignee_id", sa.Uuid(), nullable=True))
    op.create_foreign_key("fk_tickets_assignee_id_users", "tickets", "users", ["assignee_id"], ["id"], ondelete="SET NULL")
    op.create_index("ix_tickets_assignee_id", "tickets", ["assignee_id"])


def downgrade():
    op.drop_index("ix_tickets_assignee_id", table_name="tickets")
    op.drop_constraint("fk_tickets_assignee_id_users", "tickets", type_="foreignkey")
    op.drop_column("tickets", "assignee_id")
