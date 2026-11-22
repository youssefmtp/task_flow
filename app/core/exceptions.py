class RepositoryError(Exception):
    """Base exception for repository errors."""

class TaskCreationError(RepositoryError):
    pass


class TaskDeletionError(RepositoryError):
    pass

class TaskRetryError(RepositoryError):
    pass

class TaskNotFoundError(Exception):
    pass


class TaskRetryNotAllowedError(Exception):
    pass


class MaxRetriesExceededError(Exception):
    pass

class TaskDeletionNotAllowedError(Exception):
    pass