from pydantic import BaseModel

class BookRequested(BaseModel):
    isbn: int | None = None
    title: str
    author: str
    pages_num: int | None = None