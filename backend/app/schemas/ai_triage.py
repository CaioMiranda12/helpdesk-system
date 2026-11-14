from enum import Enum
from pydantic import BaseModel, Field, field_validator
from app.schemas.ticket import Priority


class TriageCategory(str, Enum):
    access = "access"
    infrastructure = "infrastructure"
    software = "software"
    hardware = "hardware"
    general = "general"


class AITriageRequest(BaseModel):
    title: str = Field(min_length=5, max_length=120)
    description: str = Field(min_length=10, max_length=2000)

    @field_validator("title", "description")
    @classmethod
    def strip_and_validate(cls, value: str, info):
        value = value.strip()
        minimum = 5 if info.field_name == "title" else 10
        if len(value) < minimum:
            raise ValueError(f"O campo deve ter pelo menos {minimum} caracteres úteis")
        return value


class AITriageResponse(BaseModel):
    priority: Priority
    category: TriageCategory
    reason: str
    provider: str = "mock"
