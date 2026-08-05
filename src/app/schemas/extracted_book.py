from pydantic import BaseModel, ConfigDict

from src.app.domain.book.models import Book, ReadingStatus

class ExtractedBook(BaseModel):
    model_config = ConfigDict(extra='forbid')

    isbn: int | None = None
    title: str
    author: str
    pages_num: int | None = None

    def to_book(self, reading_status: ReadingStatus) -> Book:
        return Book(
            title=self.title,
            author=self.author,
            pages_num=self.pages_num,
            reading_status=reading_status,
            isbn=self.isbn
        )

class ExtractedBooks(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    books: list[ExtractedBook]