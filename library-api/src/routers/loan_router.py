from fastapi import APIRouter, status, Depends
from typing import List, Optional
from controllers.loan_controller import LoanController
from schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse, MessageResponse, LoanReturnResponse
from middleware.auth import verify_credentials

router = APIRouter(
    prefix="/loans",
    tags=["Loans"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(verify_credentials)],
)


@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
async def create_loan(loan: LoanCreate):
    """
    Create a new loan (borrow a book)

    - **member_id**: ID of the member (required)
    - **book_id**: ID of the book to borrow (required)
    - **return_deadline**: Date when book should be returned (required, max 30 days from now)

    Business Rules:
    - Book must be available (stock > 0)
    - Member cannot have active loans
    - Maximum loan duration is 30 days
    - One book per loan
    """
    return LoanController.create_loan(loan)


@router.get("/", response_model=List[LoanDetailResponse])
async def get_loans(skip: int = 0, limit: int = 100, status: Optional[str] = None):
    """
    Get loans with detailed information for admin tracking

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    - **status**: Filter by loan status: ACTIVE, RETURNED, OVERDUE (optional)
    """
    return LoanController.get_loans(skip=skip, limit=limit, status=status)


@router.get("/active", response_model=List[LoanDetailResponse])
async def get_active_loans():
    """
    Get all active loans
    """
    return LoanController.get_active_loans()


@router.get("/overdue", response_model=List[LoanDetailResponse])
async def get_overdue_loans():
    """
    Get all overdue loans (past deadline but not returned)
    """
    return LoanController.get_overdue_loans()


@router.get("/{loan_id}", response_model=LoanDetailResponse)
async def get_loan(loan_id: int):
    """
    Get detailed information about a specific loan

    - **loan_id**: The ID of the loan to retrieve
    """
    return LoanController.get_loan_by_id(loan_id)


@router.put("/{loan_id}/return", response_model=LoanReturnResponse)
async def return_book(loan_id: int):
    """
    Return a borrowed book

    - **loan_id**: The ID of the loan to return

    This will:
    - Mark the loan as returned
    - Set the actual return date
    - Increase the book's stock
    - Calculate if the return was late
    """
    return LoanController.return_book(loan_id)