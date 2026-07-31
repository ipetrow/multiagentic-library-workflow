from dataclasses import dataclass, asdict
from enum import Enum

from src.app.schemas.extracted_book import ExtractedBook

@dataclass
class BookValidationResult:
    valid: bool
    normalized_book: ExtractedBook
    errors: list[str]

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class BooksValidationResult:
    valid: bool
    results: list[BookValidationResult]