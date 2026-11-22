from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.repositories.task_repository import TaskRepository
from app.models.task import Task


class SqlAlchemyTaskRepository(TaskRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, task_id: UUID) -> Task | None:
        statement = select(Task).where(Task.id == task_id)
        task = self.session.scalar(statement)

        if task is not None:
            return task

        return None

    def find_all(self) -> list[Task]:
        statement = select(Task)
        tasks = list(self.session.scalars(statement).all())

        if tasks:
            return tasks
        return []

    def add(self, task:Task) -> Task:
        self.session.add(task)

    def delete(self, task_id:UUID) -> None:
        task = self.get_by_id(task_id)

        if task is not None:
            self.session.delete(task)

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()