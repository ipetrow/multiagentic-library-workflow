from dataclasses import dataclass
from enum import Enum

from src.app.domain.book.models import Book

class BooksValidationResult:
    valid: bool
    normalized_book: Book | None
    errors: list[str]