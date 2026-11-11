from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator

class ActivityKind(str, Enum):
    comment = "comment"
    status = "status"
    assignment = "assignment"

class CommentCreate(BaseModel):
    body: str = Field(min_length=1, max_length=2000)

    @field_validator("body")
    @classmethod
    def strip_body(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Comentário não pode estar vazio")
        return value

class ActivityAuthor(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str

class ActivityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    ticket_id: UUID
    kind: ActivityKind
    body: str | None
    old_value: str | None
    new_value: str | None
    author: ActivityAuthor
    created_at: datetime
