from pydantic import BaseModel

class BookResponse(BaseModel):
    isbn: int | None = None
    title: str
    author: str
    pages_num: int | None = None

class BooksResponse(BaseModel):
    books: list[BookResponse]