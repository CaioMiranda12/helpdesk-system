import uuid
from sqlalchemy.schema import CreateTable
from app.models.ticket import Ticket


def test_ticket_model_has_expected_columns():
    assert set(Ticket.__table__.columns.keys()) == {"id", "title", "description", "priority", "status", "assignee_id", "created_at", "updated_at"}
    assert Ticket.__table__.primary_key.columns.keys() == ["id"]


def test_ticket_uuid_default_is_generated():
    generated = Ticket.__table__.c.id.default.arg(None)
    assert isinstance(generated, uuid.UUID)


def test_ticket_postgres_schema_compiles():
    from sqlalchemy.dialects import postgresql
    ddl = str(CreateTable(Ticket.__table__).compile(dialect=postgresql.dialect()))
    assert "CREATE TABLE tickets" in ddl
    assert "TIMESTAMP WITH TIME ZONE" in ddl
