from pydantic import BaseModel, ConfigDict


class StatusCounts(BaseModel):
    open: int = 0
    in_progress: int = 0
    resolved: int = 0


class PriorityCounts(BaseModel):
    low: int = 0
    medium: int = 0
    high: int = 0


class DashboardSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    total: int
    by_status: StatusCounts
    by_priority: PriorityCounts
