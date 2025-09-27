from fastapi import APIRouter, status, Depends
from typing import List
from controllers.book_controller import BookController
from schemas.book_schema import BookCreate, BookUpdate, BookResponse
from schemas.loan_schema import MessageResponse
from middleware.auth import verify_credentials

router = APIRouter(
    prefix="/books",
    tags=["Books"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(verify_credentials)],
)


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    """
    Create a new book entry

    - **title**: Book title (required)
    - **isbn**: ISBN (required, at least 10 characters)
    - **stock**: Initial stock quantity (default: 0)
    """
    return BookController.create_book(book)


@router.get("/", response_model=List[BookResponse])
async def get_books(skip: int = 0, limit: int = 100):
    """
    Get all books with pagination

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    return BookController.get_books(skip=skip, limit=limit)


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int):
    """
    Get a specific book by ID

    - **book_id**: The ID of the book to retrieve
    """
    return BookController.get_book_by_id(book_id)


@router.get("/isbn/{isbn}", response_model=BookResponse)
async def get_book_by_isbn(isbn: str):
    """
    Get a book by ISBN

    - **isbn**: The ISBN of the book to retrieve
    """
    return BookController.get_book_by_isbn(isbn)


@router.put("/{book_id}", response_model=BookResponse)
async def update_book(book_id: int, book_update: BookUpdate):
    """
    Update a book's information

    - **book_id**: The ID of the book to update
    - **title**: New book title (optional)
    - **isbn**: New ISBN (optional)
    - **stock**: New stock quantity (optional)
    """
    return BookController.update_book(book_id, book_update)


@router.delete("/{book_id}", response_model=MessageResponse)
async def delete_book(book_id: int):
    """
    Delete a book

    - **book_id**: The ID of the book to delete

    Note: Cannot delete books with active loans
    """
    return BookController.delete_book(book_id)