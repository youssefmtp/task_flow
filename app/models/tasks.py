from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import String, Integer, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.db.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Task(Base):
    __tablename__ = "tasks"

    VALID_STATUSES = {"PENDING", "RUNNING", "SUCCESS", "FAILED"}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    task_type: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="PENDING")
    payload: Mapped[dict] = mapped_column(JSONB)
    result: Mapped[dict | None] = mapped_column(JSONB, default=None)
    error_message: Mapped[str | None] = mapped_column(Text, default=None)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    max_retries: Mapped[int] = mapped_column(Integer, default=3)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow
    )
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None
    )

    # Validations

    @validates("task_type")
    def validate_task_type(self, key, value):
        if not value:
            raise ValueError("task_type is required")
        return value

    @validates("payload")
    def validate_payload(self, key, value):
        if not isinstance(value, dict):
            raise ValueError("payload must be a dictionary")
        return value

    @validates("max_retries")
    def validate_max_retries(self, key, value):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError("max_retries cannot be negative")
        return value

    @validates("retry_count")
    def validate_retry_count(self, key, value):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError("retry_count must be a non-negative integer")
        return value

    @validates("status")
    def validate_status(self, key, value):
        if value not in self.VALID_STATUSES:
            raise ValueError("Invalid task status")
        return value