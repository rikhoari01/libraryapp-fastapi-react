from fastapi import HTTPException, status
from typing import List, Optional
from datetime import date
from models.loan_model import LoanModel
from models.book_model import BookModel
from models.member_model import MemberModel
from schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse, MessageResponse, LoanReturnResponse
from schemas.member_schema import MemberResponse
from utils.response import response_success, response_error

class LoanController:

    @staticmethod
    def create_loan(loan_data: LoanCreate) -> LoanResponse:
        """Create a new loan (borrow a book)"""
        try:
            # Check if member exists
            member = MemberModel.get_by_id(loan_data.member_id)
            if not member:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Member not found"
                )

            # Check if book exists
            book = BookModel.get_by_id(loan_data.book_id)
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found"
                )

            # Check if book is available (stock > 0)
            if not BookModel.check_availability(loan_data.book_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Book is not available (out of stock)"
                )

            # Check if member has active loans
            if MemberModel.has_active_loan(loan_data.member_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Member already has an active loan"
                )

            # Create the loan
            created_loan = LoanModel.create(
                member_id=loan_data.member_id,
                book_id=loan_data.book_id,
                return_deadline=loan_data.return_deadline.isoformat()
            )

            if not created_loan:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to create loan"
                )

            # Update book stock
            BookModel.update_stock(loan_data.book_id, -1)

            result = LoanResponse(**created_loan).dict()
            return response_success(message=f"Loan for member with card id {member['id_card_number']} created  successfully", data=result)
        except HTTPException as e:
            return response_error(code=e.status_code, message=e.detail)

    @staticmethod
    def get_loans(skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[LoanDetailResponse]:
        """Get loans with detailed information for admin tracking"""
        loans = LoanModel.get_detailed_loans(skip=skip, limit=limit, status=status)
        result = [LoanDetailResponse(**loan).dict() for loan in loans]
        return response_success('Loans retrieved successfully', data=result)

    @staticmethod
    def get_loan_by_id(loan_id: int) -> LoanDetailResponse:
        """Get detailed information about a specific loan"""
        try:
            loan = LoanModel.get_detailed_by_id(loan_id)
            if not loan:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Loan not found"
                )
            result = LoanDetailResponse(**loan)
            return response_success('Loan retrieved successfully', data=result)
        except HTTPException as e:
            return response_error(code=e.status_code, message=e.detail)

    @staticmethod
    def return_book(loan_id: int) -> LoanReturnResponse:
        """Return a borrowed book"""
        try:
            # Get loan details before returning
            loan_detail = LoanModel.get_detailed_by_id(loan_id)
            if not loan_detail:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Loan not found"
                )

            if loan_detail['status'] != 'ACTIVE':
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Loan is not active"
                )

            # Return the book
            returned_loan = LoanModel.return_book(loan_id)
            if not returned_loan:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to return book"
                )

            member = MemberModel.get_by_id_card(loan_detail['member_id_card'])

            # Update book stock
            book_id = returned_loan['book_id']
            BookModel.update_stock(book_id, 1)

            # Calculate if return was late
            return_deadline = date.fromisoformat(returned_loan['return_deadline'])
            actual_return = date.fromisoformat(returned_loan['actual_return_date'])
            was_late = actual_return > return_deadline
            days_late = (actual_return - return_deadline).days if was_late else None

            result = LoanReturnResponse(
                book_id=book_id,
                card_member_id=member['id_card_number'],
                return_date=returned_loan['actual_return_date'],
                was_late=was_late,
                days_late=days_late if was_late else None
            ).dict()
            return response_success(message='Book returned successfully', data=result)
        except HTTPException as e:
            return response_error(code=e.status_code, message=e.detail)

    @staticmethod
    def get_overdue_loans() -> List[LoanDetailResponse]:
        """Get all overdue loans"""
        loans = LoanModel.get_overdue_loans()
        # Convert to detailed format
        detailed_loans = []
        for loan in loans:
            detailed_loan = LoanModel.get_detailed_by_id(loan['id'])
            if detailed_loan:
                detailed_loans.append(LoanDetailResponse(**detailed_loan))
        result = detailed_loans
        return response_success(message='Loans retrieved successfully', data=result)

    @staticmethod
    def get_active_loans() -> List[LoanDetailResponse]:
        """Get all active loans"""
        loans = LoanModel.get_detailed_loans(status='ACTIVE', limit=1000)
        result = [LoanDetailResponse(**loan).dict() for loan in loans]
        return response_success(message='Loans retrieved successfully', data=result)