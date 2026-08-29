from pydantic import BaseModel

from src.app.schemas.extracted_book import ExtractedBook

class BookValidationResult(BaseModel):
    valid: bool
    book: ExtractedBook
    errors: list[str]

class BooksValidationResult(BaseModel):
    valid: bool
    results: list[BookValidationResult]

class FinishedMonthValidationResult(BaseModel):
    valid: bool
    value: str | None = None
    error: str | None = None
    