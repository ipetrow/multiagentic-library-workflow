from pydantic import BaseModel, ConfigDict, Field

from src.app.domain.book.models import Book

class ExtractedBook(BaseModel):
    model_config = ConfigDict(extra='forbid')

    isbn: str | None = Field(
        default=None,
        description="Book's ISBN."
    )
    title: str = Field(
        description="Book's title."
    )
    author: str = Field(
        description="Book's author. ONLY a single author only is supported."
    )
    pages_num: int | None = Field(
        default=None,
        description="The book's number of pages."
    )
    finished_month: str | None = Field(
        default=None,
        description="The month the book has been finished, in the format YYYY-MM. Example: '2023-03'."
    )

    def to_book(self) -> Book:
        return Book(
            title=self.title,
            author=self.author,
            pages_num=self.pages_num,
            isbn=self.isbn,
            finished_month=self.finished_month
        )

class ExtractedBooks(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    books: list[ExtractedBook]