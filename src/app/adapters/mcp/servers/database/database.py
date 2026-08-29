import json
import sqlite3
from datetime import date

from .exceptions import BookNotFoundError

from src.app.domain.book.models import Book, ReadingStatus

class Database: 

    def __init__(self, db_path: str):
        self.db_path = db_path

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)
    
    def get_all_books(self) -> str:
        """
        Gets all the books from the database.

        Returns:
            A list with all the books in the database.
        """

        with self.connect() as conn:
            cur = conn.cursor()

            query = "SELECT * FROM books"

            books = [ 
                {
                    "isbn": row[1],
                    "title": row[2],
                    "author": row[3],
                    "pages_num": row[4],
                    "finished_month": row[5],
                    "reading_status": row[6]
                }
                for row in cur.execute(query)
            ]

            response = {
                "books": books
            }

            books_json = json.dumps(response, indent=2)

        return books_json

    def insert_book(self, book: Book) -> int:
        """
        Insert a new book in the database.

        Args: 
            book: A book to be inserted.

        Returns:
            id: The inserted book id
        """

        query="""
            INSERT INTO books (
                isbn, title, author, pages_num, finished_month, reading_status
            ) VALUES (?, ?, ?, ?, ?, ?)
        """

        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute(query, (book.isbn, book.title, book.author, book.pages_num, book.finished_month, book.reading_status))
            conn.commit()

            return cur.lastrowid

    def is_duplicate(self, title: str, author: str) -> bool:
        query = """
            SELECT 1 
            FROM books
            WHERE title = ? AND author = ?
            LIMIT 1
        """

        with self.connect() as conn:
            cur = conn.cursor()
            return cur.execute(query, (title, author)).fetchone() is not None
    
    def update_reading_status(self, book_id: int, reading_status: ReadingStatus) -> None:

        query = """
            UPDATE books 
            SET reading_status = ? 
            WHERE id = ?
        """

        with self.connect() as conn:
            cur = conn.cursor().execute(query, (reading_status, book_id))

            if cur.rowcount == 0:
                raise BookNotFoundError()

            conn.commit()

    def update_finished_month(self, book_id: int, finished_date: date) -> None:
    
        query = """
            UPDATE books 
            SET finished_month = ? 
            WHERE id = ?
        """

        with self.connect() as conn:
            cur = conn.cursor().execute(query, (finished_date, book_id))

            if cur.rowcount == 0:
                raise BookNotFoundError()

            conn.commit()

    def get_id(self, title: str, author: str) -> int | None:
        query="""
            SELECT id 
            FROM books
            WHERE title = ? AND author = ?
        """

        with self.connect() as conn:
            row = conn.cursor().execute(query, (title, author)).fetchone()

        return row[0] if row else None

    def delete_books_data(self) -> None:
        """
        Delete the books data.

        Returns:
            None
        """

        query = "DELETE FROM books"

        with self.connect() as conn:
            conn.cursor().execute(query)
            conn.commit()
