from dataclasses import dataclass
from enum import Enum

from src.app.schemas.extracted_book import ExtractedBook

@dataclass
class BookValidationResult:
    valid: bool
    normalized_book: ExtractedBook
    errors: list[str]

@dataclass
class BooksValidationResult:
    valid: bool
    results: list[BookValidationResult]