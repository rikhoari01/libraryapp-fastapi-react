from fastapi import HTTPException, status
from typing import List
from models.book_model import BookModel
from models.loan_model import LoanModel
from schemas.book_schema import BookCreate, BookUpdate, BookResponse
from schemas.loan_schema import MessageResponse
from utils.response import response_success, response_error

class BookController:

    @staticmethod
    def create_book(book_data: BookCreate) -> BookResponse:
        """Create a new book"""
        try:
            # Check if ISBN already exists
            existing_book = BookModel.get_by_isbn(book_data.isbn)
            if existing_book:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ISBN already exists"
                )

            created_book = BookModel.create(
                title=book_data.title,
                isbn=book_data.isbn,
                stock=book_data.stock
            )

            if not created_book:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to create book"
                )

            result = BookResponse(**created_book).dict()
            return response_success(message="Created book successfully", data=result)
        except HTTPException as e:
            return response_error(code=e.status_code, message=e.detail)

    @staticmethod
    def get_books(skip: int = 0, limit: int = 100) -> List[BookResponse]:
        """Get all books with pagination"""
        books = BookModel.get_all(skip=skip, limit=limit)
        result = [BookResponse(**book).dict() for book in books]

        return response_success(message="Books retrieved successfully", data=result)

    @staticmethod
    def get_book_by_id(book_id: int) -> BookResponse:
        """Get a specific book by ID"""
        try:
            book = BookModel.get_by_id(book_id)
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found"
                )

            result = BookResponse(**book).dict()
            return response_success(message="Books retrieved successfully", data=result)
        except HTTPException as e:
            return response_error(code=e.status_code, message=e.detail)


    @staticmethod
    def get_book_by_isbn(isbn: str) -> BookResponse:
        """Get a book by ISBN"""
        try:
            book = BookModel.get_by_isbn(isbn)
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found"
                )

            result = BookResponse(**book).dict()
            return response_success(message="Books retrieved successfully", data=result)
        except HTTPException as e:
            return response_error(code=e.status_code, message=e.detail)

    @staticmethod
    def update_book(book_id: int, book_update: BookUpdate) -> BookResponse:
        """Update a book's information"""
        try:
            # Check if book exists
            if not BookModel.get_by_id(book_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found"
                )

            # Check if ISBN is being changed and already exists
            if book_update.isbn:
                existing_book = BookModel.get_by_isbn(book_update.isbn)
                if existing_book and existing_book['id'] != book_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="ISBN already exists"
                    )

            update_data = book_update.dict(exclude_unset=True)
            updated_book = BookModel.update(book_id, **update_data)

            if not updated_book:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to update book"
                )

            result = BookResponse(**updated_book).dict()
            return response_success(message="Book updated successfully", data=result)
        except HTTPException as e:
            return response_error(code=e.status_code, message=e.detail)

    @staticmethod
    def delete_book(book_id: int):
        """Delete a book"""
        try:
            success = BookModel.delete(book_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found"
                )
            return response_success(message="Book deleted successfully")
        except HTTPException as e:
            return response_error(code=e.status_code, message=e.detail)