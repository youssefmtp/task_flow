import pytest
from app.models.task import Task
from app.core.exceptions import TaskRetryNotAllowedError, TaskDeletionNotAllowedError, TaskCreationError
from sqlalchemy.exc import SQLAlchemyError

def test_create_email(service, email_payload):

    result = service.create_task(
        task_type="send_email",
        payload=email_payload
    )

    assert isinstance(result, Task)
    assert result.task_type == "send_email"
    assert result.payload == email_payload
    assert result.status == "PENDING"

def test_get_task(service, repository, email_payload):

    task = Task(task_type="send_email", payload = email_payload)

    repository.get_by_id.return_value = task

    result = service.get_task(task.id)

    assert isinstance(result, Task)
    assert result == task
    repository.get_by_id.assert_called_once_with(task.id)


def test_get_task_not_found(service, repository):

    repository.get_by_id.return_value = None
    result = service.get_task(0)

    assert result is None 

def test_list_tasks(service, repository, email_payload):
    task1 = Task(task_type="send_email", payload=email_payload)
    task2 = Task(task_type="generate_report", payload={"format": "csv"})

    repository.find_all.return_value = [task1, task2]

    result = service.list_tasks()

    assert isinstance(result, list)
    assert len(result) == 2


def test_retry_task(service, repository, email_payload):

    task = Task(task_type="send_email", payload = email_payload)

    repository.get_by_id.return_value = task

    task.status = "FAILED"
    task.retry_count = 0
    task.max_retries = 3

    result = service.retry_task(task.id)

    assert isinstance(result, Task)
    assert result.status == "PENDING" 

def test_retry_task_not_allowed(service, repository, email_payload):

    task = Task(task_type="send_email", payload=email_payload)
    task.status = "SUCCESS"

    repository.get_by_id.return_value = task

    with pytest.raises(TaskRetryNotAllowedError):
        service.retry_task(task.id)

    repository.commit.assert_not_called()



def test_delete_task(service, repository, email_payload):
    task = Task(task_type="send_email", payload=email_payload)
    
    repository.get_by_id.return_value = task

    result = service.delete_task(task.id)

    assert result is None


def test_delete_running_task(service, repository, email_payload):
    task = Task(task_type="send_email", payload=email_payload)

    task.status = "RUNNING"
    
    repository.get_by_id.return_value = task

    with pytest.raises(TaskDeletionNotAllowedError):
        service.delete_task(task.id)


def test_create_task_database_error(service, repository, email_payload):
    repository.commit.side_effect = SQLAlchemyError("Database error")

    with pytest.raises(TaskCreationError):
        service.create_task(
            task_type="send_email",
            payload=email_payload
        )

    repository.add.assert_called_once()
    repository.commit.assert_called_once()
    repository.rollback.assert_called_once()
