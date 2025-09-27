from config.database import get_db_connection
from typing import List, Optional, Dict, Any
import sqlite3

class BookModel:

    @staticmethod
    def create(title: str, isbn: str, stock: int = 0) -> Optional[Dict[str, Any]]:
        """Create a new book"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO books (title, isbn, stock) VALUES (?, ?, ?)",
                    (title, isbn, stock)
                )
                book_id = cursor.lastrowid
                conn.commit()

                # Return the created book
                return BookModel.get_by_id(book_id)
        except sqlite3.IntegrityError:
            return None

    @staticmethod
    def get_all(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all books with pagination"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books LIMIT ? OFFSET ?", (limit, skip))
            books = cursor.fetchall()
            return [dict(book) for book in books]

    @staticmethod
    def get_by_id(book_id: int) -> Optional[Dict[str, Any]]:
        """Get book by ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
            book = cursor.fetchone()
            return dict(book) if book else None

    @staticmethod
    def get_by_isbn(isbn: str) -> Optional[Dict[str, Any]]:
        """Get book by ISBN"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
            book = cursor.fetchone()
            return dict(book) if book else None

    @staticmethod
    def update(book_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update book information"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()

                # Check if book exists
                if not BookModel.get_by_id(book_id):
                    return None

                # Build update query
                update_fields = []
                values = []

                for field in ['title', 'isbn', 'stock']:
                    if field in kwargs and kwargs[field] is not None:
                        update_fields.append(f"{field} = ?")
                        values.append(kwargs[field])

                if not update_fields:
                    return BookModel.get_by_id(book_id)

                update_fields.append("updated_at = datetime('now')")
                values.append(book_id)

                query = f"UPDATE books SET {', '.join(update_fields)} WHERE id = ?"
                cursor.execute(query, values)
                conn.commit()

                return BookModel.get_by_id(book_id)
        except sqlite3.IntegrityError:
            return None

    @staticmethod
    def delete(book_id: int) -> bool:
        """Delete a book"""
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Check if book exists
            if not BookModel.get_by_id(book_id):
                return False

            # Check for active loans
            cursor.execute(
                "SELECT COUNT(*) FROM loans WHERE book_id = ? AND status = 'ACTIVE'",
                (book_id,)
            )
            if cursor.fetchone()[0] > 0:
                raise ValueError("Cannot delete book with active loans")

            cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def update_stock(book_id: int, change: int) -> bool:
        """Update book stock (positive for return, negative for borrow)"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE books SET stock = stock + ?, updated_at = datetime('now') WHERE id = ?",
                (change, book_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def check_availability(book_id: int) -> bool:
        """Check if book is available for borrowing"""
        book = BookModel.get_by_id(book_id)
        return book and book['stock'] > 0