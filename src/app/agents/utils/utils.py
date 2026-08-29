import re

from src.app.schemas.extracted_book import ExtractedBook
from src.app.domain.book.models import Book

from ..models.models import (
    BookValidationResult,
    BooksValidationResult,
    FinishedMonthValidationResult
)

def prepare_books_insertion(validated_extracted_books: list[ExtractedBook]) -> list[Book]:
    return [
        validated_book.to_book()
        for validated_book in validated_extracted_books
    ]

def validate_extracted_books(extracted_books: list[ExtractedBook]) -> BooksValidationResult:

    validated_books: list[BookValidationResult] = []

    for book in extracted_books:
        errors: list[str] = []

        title = book.title
        author = book.author
        pages_num = book.pages_num
        isbn = book.isbn
        finished_month = book.finished_month

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
            normalized_isbn = _normalize_isbn(isbn)

            if normalized_isbn.isdigit():
                book.isbn = normalized_isbn
            else:
                errors.append("Invalid ISBN containing not only digits")

        if finished_month:
            finished_month_validation_result = normalize_finished_month(finished_month)

            if finished_month_validation_result.valid:
                book.finished_month = finished_month_validation_result.value
            else:
                errors.append(finished_month_validation_result.error)

        is_book_valid = True if not errors else False

        validated_books.append(
            BookValidationResult(
                valid = is_book_valid,
                book = book,
                errors = errors
            )
        )

    return BooksValidationResult(
        valid = all(validated_book.valid for validated_book in validated_books),
        results = validated_books
    )

def _normalize_text(text: str) -> str:
    return " ".join(text.strip().split())

def _normalize_isbn(isbn: str | None) -> str | None:

    if not isbn:
        return None

    return isbn.replace("-", "").replace(" ", "").upper()

def normalize_finished_month(finished_month: str) -> FinishedMonthValidationResult:
    """
    Convert the month the book has been finished to a date in the format 'YYYY-MM-DD'.
    The normalization is done for an easier integration with the database DATE type. 
    Being not of other importance, the set day is always the first of the month.

    Example: '2023-03' -> '2023-03-01'.

    Args:
        finished_month: The month in which the book has been finished. Format: 'YYYY-MM'.
    
    Returns:
        The validation result.
    """


    if not re.fullmatch(r"\d{4}-\d{2}", finished_month):
        return FinishedMonthValidationResult(
            valid=False,
            error="Invalid month format. Supported format YYYY-MM."
        )

    return FinishedMonthValidationResult(
        valid=True,
        value=finished_month + "-01"
    )
