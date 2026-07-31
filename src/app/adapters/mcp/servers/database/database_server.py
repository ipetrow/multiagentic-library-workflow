import json

from mcp.server.fastmcp import FastMCP

from src.app.domain.book.models import ReadingStatus, Book
from src.app.config import get_settings

from .database import Database
from .exceptions import BookNotFoundError

db = Database(get_settings().database_path)

# Initialize FastMCP server
mcp = FastMCP("bookslog.db")

@mcp.tool()
def get_all_books() -> str:
    """
    Gets all the books from the database.

    Returns:
        A list with all the books in the database.
    """

    return db.get_all_books()

@mcp.tool()
def insert_books(books: list[Book]) -> str:
    inserted_books = {
        "books_insertion_status": []
    }

    for book in books:
        if db.is_duplicate(title=book.title, author=book.author):
            inserted_books["books_insertion_status"].append({
                "success": False,
                "book": {
                    "title": book.title,
                    "author": book.author
                },
                "error": "BookDuplicationError",
                "message": "Book with same title and author already exists"
            })

        db.insert_book(book=book)
        
        inserted_books["books_insertion_status"].append({
            "success": True,
            "book": {
                "title": book.title,
                "author": book.author
            },
            "message": "Book added successfully"
        })

    return json.dumps(inserted_books)

@mcp.tool()
def update_book_reading_status(book: Book, reading_status: ReadingStatus) -> str:
    book_id = db.get_id(title=book.title, author=book.author)

    if book_id is None:
        update_status = {
            "success": False,
            "book": {
                "title": book.title,
                "author": book.author,
                "reading_status": book.reading_status
            },
            "error": "BookNotFoundError",
            "message": "Book not found in database."
        }
        
    try:
        db.update_reading_status(book_id=book_id, reading_status=reading_status)
        update_status = {
            "success": True,
            "book": {
                "title": book.title,
                "author": book.author,
                "reading_status": book.reading_status
            },
            "message": "Book reading status updated successfully."
        }
    except BookNotFoundError as ex:
        update_status = {
            "success": False,
            "book": {
                "title": book.title,
                "author": book.author,
                "reading_status": book.reading_status
            },
            "error": "BookNotFoundError",
            "message": "Book not found in database."
        }

    return json.dumps(update_status)

if __name__ == "__main__":
    mcp.run(transport="stdio")