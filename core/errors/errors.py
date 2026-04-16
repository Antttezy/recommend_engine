class BaseError(Exception):
    """Base exception class for all core logic exceptions"""
    ...


class NotFoundError(BaseError):
    """Thrown when requested item is not found"""
    ...


class AlreadyExistsError(BaseError):
    """Thrown when caller tries to create item with id of already existing one"""
    ...
