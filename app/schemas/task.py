
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class TaskCreate(BaseModel):
    task_type: str
    payload: dict


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    task_type: str
    status: str
    payload: dict
    result: dict | None = None
    error_message: str | None = None
    retry_count: int
    max_retries: int
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int
