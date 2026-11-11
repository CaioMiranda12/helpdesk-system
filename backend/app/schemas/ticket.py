from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Status(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"

class TicketCreate(BaseModel):
    title: str = Field(min_length=5, max_length=120)
    description: str = Field(min_length=10, max_length=2000)
    priority: Priority = Priority.medium

    @field_validator("title", "description")
    @classmethod
    def validate_text(cls, value: str, info):
        value = value.strip()
        minimum = 5 if info.field_name == "title" else 10
        if len(value) < minimum:
            raise ValueError(f"O campo deve ter pelo menos {minimum} caracteres úteis")
        return value

class TicketUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=5, max_length=120)
    description: str | None = Field(default=None, min_length=10, max_length=2000)
    priority: Priority | None = None

    @field_validator("title", "description")
    @classmethod
    def validate_text(cls, value: str | None, info):
        if value is None:
            raise ValueError("Não é permitido informar null")
        value = value.strip()
        minimum = 5 if info.field_name == "title" else 10
        if len(value) < minimum:
            raise ValueError(f"O campo deve ter pelo menos {minimum} caracteres úteis")
        return value

    @model_validator(mode="after")
    def not_empty(self):
        if not self.model_fields_set:
            raise ValueError("Informe ao menos um campo para atualizar")
        if any(getattr(self, field) is None for field in self.model_fields_set):
            raise ValueError("Não é permitido informar null")
        return self

class TicketStatusUpdate(BaseModel):
    status: Status

class TicketAssigneeUpdate(BaseModel):
    assignee_id: UUID | None

class TicketAssigneeRead(BaseModel):
    id: UUID
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class TicketRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    description: str
    priority: Priority
    status: Status
    assignee_id: UUID | None = None
    assignee: TicketAssigneeRead | None = None
    created_at: datetime
    updated_at: datetime
