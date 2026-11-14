from typing import Literal

from pydantic import BaseModel, Field


class TriageRequest(BaseModel):
    title: str = Field(min_length=5, max_length=200)
    description: str = Field(min_length=10, max_length=5000)


class TriageSuggestion(BaseModel):
    category: Literal[
        "hardware",
        "software",
        "network",
        "access",
        "other",
    ]
    priority: Literal["low", "medium", "high"]
    reason: str = Field(min_length=1, max_length=500)