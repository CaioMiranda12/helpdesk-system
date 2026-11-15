from pydantic import BaseModel, Field


class AIActivitySummaryResponse(BaseModel):
    summary: str = Field(min_length=10, max_length=1600)
    provider: str
    activities_considered: int = Field(ge=1, le=50)
