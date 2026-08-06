from src.app.schemas.extracted_book import ExtractedBook
from src.app.domain.book.models import Book

from ..models.models import (
    BookValidationResult,
    BooksValidationResult
)

def prepare_books_insertion(validated_extracted_books: list[ExtractedBook]) -> list[Book]:
    return [
        validated_book.to_book() 
        for validated_book in validated_extracted_books
    ]

def validate_extracted_books(extracted_books: list[ExtractedBook]) -> BooksValidationResult:

    validated_books: list[BookValidationResult] = []
    are_all_books_valid = True

    for book in extracted_books:
        errors: list[str] = []

        title = book.title
        author = book.author
        pages_num = book.pages_num
        isbn = book.isbn

        if title:
            book.title = _normalize_text(title)
        else:
            errors.append("Missing title")

        if author:
            book.author = _normalize_text(author)
        else:
            errors.append("Missing author")

        if not pages_num:
            errors.append("Missing pages number")

        if isbn:
            book.isbn = _normalize_isbn(isbn)

        is_book_valid = "true" if not errors else "false"

        validated_books.append(
            BookValidationResult(
                valid = is_book_valid,
                normalized_book = book,
                errors = errors
            )
        )

        if are_all_books_valid:
            are_all_books_valid = is_book_valid

    return BooksValidationResult(
        valid = are_all_books_valid,
        results = validated_books
    )

def _normalize_text(text: str) -> str:
    return " ".join(text.strip().split())

def _normalize_isbn(isbn: str | None) -> str | None:

    if not isbn:
        return None

    return isbn.replace("-", "").replace(" ", "").upper()