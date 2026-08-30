import json
from datetime import date

from mcp.server.fastmcp import FastMCP

from src.app.domain.book.models import ReadingStatus, Book
from src.app.config import get_settings

from .database import Database
from .models import MonthlyStatistic
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
    """
        Insert new books to the database.

        Args: 
            books: A list with all the books to be inserted.

        Returns:
            The result of the insert operation in a JSON string format.
    """
    inserted_books = {
        "books_insertion_status": []
    }

    for book in books:
        if not db.is_duplicate(title=book.title, author=book.author):
            db.insert_book(book=book)

            inserted_books["books_insertion_status"].append({
                "success": True,
                "book": {
                    "title": book.title,
                    "author": book.author
                },
                "message": "Book added successfully"
            })
        else:
            inserted_books["books_insertion_status"].append({
                "success": False,
                "book": {
                    "title": book.title,
                    "author": book.author
                },
                "error": "BookDuplicationError",
                "message": "Book with same title and author already exists"
            })        

    return json.dumps(inserted_books)

@mcp.tool()
def update_book_reading_status(
    title: str, 
    author: str, 
    reading_status: ReadingStatus, 
    new_reading_status: ReadingStatus
) -> str:
    """
        Update book's reading status by title and author

        Args: 
            title: book's title
            author: book's author
            reading_status: book's reading status
            new_reading_status: the new reading status with which the book will be update
        Returns:
            The result of the update operation in a JSON string format.
    """

    book_id = db.get_id(title=title, author=author)

    if book_id is None:
        update_status = {
            "success": False,
            "book": {
                "title": title,
                "author": author,
                "reading_status": reading_status
            },
            "error": "BookNotFoundError",
            "message": "Book not found in database."
        }
        
    try:
        db.update_reading_status(book_id=book_id, reading_status=new_reading_status)
        update_status = {
            "success": True,
            "book": {
                "title": title,
                "author": author,
                "reading_status": new_reading_status
            },
            "message": "Book reading status updated successfully."
        }
    except BookNotFoundError as ex:
        update_status = {
            "success": False,
            "book": {
                "title": title,
                "author": author,
                "reading_status": reading_status
            },
            "error": "BookNotFoundError",
            "message": "Book not found in database."
        }

    return json.dumps(update_status)

@mcp.tool()
def update_book_finished_month(
    title: str, 
    author: str, 
    finished_month: str
) -> str:
    """
        Update book's finished month by title and author

        Args: 
            title: book's title
            author: book's author
            finished_month: book's finished month
        Returns:
            The result of the update operation in a JSON string format.
    """

    try:
        finished_date = date.fromisoformat(finished_month)
    except ValueError:
        update_status = {
            "success": False,
            "book": {
                "title": title,
                "author": author,
                "finished": finished_month
            },
            "error": "ValueError",
            "message": "Invalid finished month format. Expected: YYYY-MM-DD."
        }

    book_id = db.get_id(title=title, author=author)

    if book_id is None:
        update_status = {
            "success": False,
            "book": {
                "title": title,
                "author": author
            },
            "error": "BookNotFoundError",
            "message": "Book not found in database."
        }
        
    try:
        db.update_finished_month(book_id=book_id, finished_date=finished_date)
        update_status = {
            "success": True,
            "book": {
                "title": title,
                "author": author,
                "finished": finished_month
            },
            "message": "Book finished month updated successfully."
        }
    except BookNotFoundError as ex:
        update_status = {
            "success": False,
            "book": {
                "title": title,
                "author": author
            },
            "error": "BookNotFoundError",
            "message": "Book not found in database."
        }

    return json.dumps(update_status)

@mcp.tool()
def get_reading_statistics(
    year: int
) -> str:
    """
        Retrieve the reading statistics for a specified year.

        Args: 
            year: the year for which the reading statistics is prepared.
        Returns:
            A JSON string describing the reading statistics for an year, grouped by month.
    """

    start_date = date(year=year, month=1, day=1)
    end_date = date(year=year + 1, month=1, day=1)

    year_statistics: list[MonthlyStatistic] = db.get_books_read_by_month(
        start_date=start_date,
        end_date=end_date
    )

    counts = {
        statistic.finished_month: statistic.count
        for statistic in year_statistics
    }

    data = []
    for month_number in range(1, 13):
        month_date = date(year, month_number, 1)

        month = month_date.strftime("%B")
        count = counts.get(month_date, 0)

        data.append(
            {
                "month": month,
                "count": count
            }
        )

    response = {
        "unit": "books",
        "year": year,
        "data": data
    }

    return json.dumps(response)

if __name__ == "__main__":
    mcp.run(transport="stdio")