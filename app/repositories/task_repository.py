from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse, TaskListResponse

class TaskRepository(ABC):

    @abstractmethod
    def get_by_id(self, task_id: UUID) -> Task | None:
        pass

    @abstractmethod
    def find_all(self) -> list[Task]:
        pass

    @abstractmethod
    def add(self, task:Task) -> Task:
        pass

    @abstractmethod
    def delete(self, id:UUID):
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass