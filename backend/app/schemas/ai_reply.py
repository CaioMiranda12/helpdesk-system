from pydantic import BaseModel, Field, field_validator


class AIReplyRequest(BaseModel):
    title: str = Field(min_length=5, max_length=120)
    description: str = Field(min_length=10, max_length=2000)

    @field_validator("title", "description")
    @classmethod
    def validate_text(cls, value: str, info):
        value = value.strip()
        minimum = 5 if info.field_name == "title" else 10
        if len(value) < minimum:
            raise ValueError(f"Mínimo de {minimum} caracteres úteis")
        return value


class AIReplyResponse(BaseModel):
    suggestion: str = Field(min_length=10, max_length=1200)
    provider: str
