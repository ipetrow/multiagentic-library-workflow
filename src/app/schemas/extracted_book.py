from pydantic import BaseModel

from domain.book.models import Book, ReadingStatus

class ExtractedBook(BaseModel):
    isbn: int | None = None
    title: str
    author: str
    pages_num: int | None = None

    def to_book(self, reading_status: ReadingStatus) -> Book:
        return Book(
            isbn=self.isbn,
            title=self.title,
            author=self.author,
            pages_num=self.pages_num,
            reading_status=reading_status
        )

class ExtractedBooks(BaseModel):
    books: list[ExtractedBook]