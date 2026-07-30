from src.app.schemas.extracted_book import ExtractedBook
from src.app.domain.book.models import Book

from ..models.models import BookValidationResult

def prepare_books_insertion(extracted_books: list[ExtractedBook]) -> list[Book]:
    pass

def validate_insert_books_data() -> BookValidationResult:
    pass

def _normalize_text(text: str) -> str:
    return " ".join(text.strip().split())

def _normalize_isbn(isbn: str | None) -> str | None:

    if not isbn:
        return None

    return isbn.replace("-", "").replace(" ", "").upper()