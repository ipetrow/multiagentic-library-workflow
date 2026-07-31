class BookError(Exception):
    """Base exception for all database errors."""

class BookNotFoundError(BookError):
    """Book not found exception."""