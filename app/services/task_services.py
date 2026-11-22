from uuid import UUID

from app.repositories.task_repository import TaskRepository
from app.models.task import Task
from app.core.exceptions import TaskNotFoundError, TaskRetryNotAllowedError, MaxRetriesExceededError, TaskDeletionNotAllowedError, TaskDeletionError, TaskCreationError, TaskRetryError
from sqlalchemy.exc import SQLAlchemyError

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, task_type:str, payload:dict) -> Task:
            task = Task(task_type = task_type, payload = payload)

            task.status = "PENDING"
            
            try:
                self.repository.add(task)
                self.repository.commit()
                return task
            except SQLAlchemyError as e:
                self.repository.rollback()
                raise TaskCreationError("Failed to create task") from e

    def get_task(self, task_id: UUID) -> Task | None:
            return self.repository.get_by_id(task_id)

    def list_tasks(self) -> list[Task]:
        return self.repository.find_all()

    def retry_task(self, task_id: UUID) -> Task:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError("Task not found.")

        if task.status != 'FAILED':
            raise TaskRetryNotAllowedError("The status does not allow a retry.")

        if task.retry_count >= task.max_retries:
            raise MaxRetriesExceededError("Maximum retry attempts reached")

        task.retry_count += 1 
        task.status = 'PENDING'
        task.error_message = None
        task.completed_at = None
        
        try:
            self.repository.commit()

            return task

        except SQLAlchemyError as e:
            self.repository.rollback()
            raise TaskRetryError("Failed to retry task") from e

    def delete_task(self, task_id: UUID) -> None:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError("Task not found.")
        if task.status == "RUNNING":
            raise TaskDeletionNotAllowedError("Deleted is not allowed for this status.")

        try:
            self.repository.delete(task_id)
            self.repository.commit()
        except SQLAlchemyError as e:
            self.repository.rollback()
            raise TaskDeletionError("Failed to delete task") from e
        
        
