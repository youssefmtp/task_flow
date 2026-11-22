from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_task_service
from app.services.task_services import TaskService
from app.schemas.task import (TaskCreate, TaskResponse, TaskListResponse)

from app.core.exceptions import (
    TaskNotFoundError,
    TaskRetryNotAllowedError,
    MaxRetriesExceededError,
    TaskDeletionNotAllowedError,
    TaskDeletionError,
    TaskCreationError,
    TaskRetryError,
)


router = APIRouter(prefix="/api", tags=["tasks"])

@router.get("/tasks", response_model=TaskListResponse)
def get_tasks(service: TaskService = Depends(get_task_service)):
    tasks = service.list_tasks()

    return {
        "tasks": tasks,
        "total": len(tasks),
    }


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: UUID, service: TaskService = Depends(get_task_service)):
    task = service.get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    return task


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service),
):
    try:
        return service.create_task(
            task_type=task_data.task_type,
            payload=task_data.payload,
        )

    except TaskCreationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


@router.post("/tasks/{task_id}/retry", response_model=TaskResponse)
def retry_task(task_id: UUID, service: TaskService = Depends(get_task_service)):
    try:
        return service.retry_task(task_id)

    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e

    except (
        TaskRetryNotAllowedError,
        MaxRetriesExceededError,
        TaskRetryError,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID, service: TaskService = Depends(get_task_service)):
    try:
        service.delete_task(task_id)

    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e

    except (
        TaskDeletionNotAllowedError,
        TaskDeletionError,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
