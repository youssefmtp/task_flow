
from __future__ import annotations

import pytest
from unittest.mock import Mock

from app.services.task_services import TaskService
from app.repositories.task_repository import TaskRepository


@pytest.fixture
def repository():
    return Mock(spec=TaskRepository)


@pytest.fixture
def service(repository: TaskRepository):
    return TaskService(repository)


@pytest.fixture
def email_payload():
    return {
        "sender": "noreply@taskflow.com",
        "recipient": "john.doe@example.com",
        "subject": "Your report is ready",
        "body": "Your monthly sales report has been successfully generated."
    }


@pytest.fixture
def report_payload():
    return {
        "user_id": 123,
        "format": "csv",
        "start_date": "2026-01-01",
        "end_date": "2026-01-31",
        "include_summary": True
    }

@pytest.fixture
def process_data_payload():
    return {
        "source": "customers_database",
        "operation": "clean",
        "remove_duplicates": True,
        "normalize": True,
        "records": [
            {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com"
            },
            {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane@example.com"
            },
            {
                "id": 3,
                "name": "John Doe",
                "email": "john@example.com"
            }
        ]
    }
