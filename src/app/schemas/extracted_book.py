from pydantic import BaseModel

class ExtractedBook(BaseModel):
    isbn: int | None = None
    title: str
    author: str
    pages_num: int | None = None

class ExtractedBooks(BaseModel):
    books: list[ExtractedBook]