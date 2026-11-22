from collections.abc import Generator
from sqlalchemy.orm import Session
from app.db.database import SessionLocal

from fastapi import Depends

from app.services.task_services import TaskService
from app.repositories.sqlalchemy_task_repository import SqlAlchemyTaskRepository

# Provides a session to the caller and closes it afterward
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db # Provides the database session to the caller.
    finally:
        db.close()


def get_task_service(db: Session = Depends(get_db), ) -> TaskService:
        repository = SqlAlchemyTaskRepository(db)
        return TaskService(repository)