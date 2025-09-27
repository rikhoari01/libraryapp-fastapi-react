from fastapi import HTTPException, status
from typing import List
from models.member_model import MemberModel
from schemas.member_schema import MemberCreate, MemberUpdate, MemberResponse
from schemas.loan_schema import MessageResponse
from utils.response import response_success, response_error

class MemberController:

    @staticmethod
    def create_member(member_data: MemberCreate) -> MemberResponse:
        """Create a new member"""
        try:
            # Check if ID card number already exists
            existing_member = MemberModel.get_by_id_card(member_data.id_card_number)
            if existing_member:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ID card number already exists"
                )

            # Check if email already exists
            existing_email = MemberModel.get_by_email(member_data.email)
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )

            created_member = MemberModel.create(
                id_card_number=member_data.id_card_number,
                name=member_data.name,
                email=member_data.email
            )

            if not created_member:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to create member"
                )

            result = MemberResponse(**created_member).dict()
            return response_success(message="Created member successfully", data=result)
        except HTTPException as e:
            return response_error(code=e.status_code, message=e.detail)

    @staticmethod
    def get_members(skip: int = 0, limit: int = 100) -> List[MemberResponse]:
        """Get all members with pagination"""
        members = MemberModel.get_all(skip=skip, limit=limit)
        result = [MemberResponse(**member).dict() for member in members]

        return response_success(message='Members retrieved successfully', data=result)

    @staticmethod
    def get_member_by_id(member_id: int) -> MemberResponse:
        """Get a specific member by ID"""
        try:
            member = MemberModel.get_by_id(member_id)
            if not member:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Member not found"
                )
            result = MemberResponse(**member).dict()
            return response_success(message="Member retrieved successfully", data=result)
        except HTTPException as e:
            return response_error(code=e.status_code, message=e.detail)

    @staticmethod
    def get_member_by_id_card(id_card_number: str) -> MemberResponse:
        """Get a member by ID card number"""
        try:
            member = MemberModel.get_by_id_card(id_card_number)
            if not member:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Member not found"
                )
            result = MemberResponse(**member).dict()
            return response_success(message="Member retrieved successfully", data=result)
        except HTTPException as e:
            return response_error(code=e.status_code, message=e.detail)

    @staticmethod
    def update_member(member_id: int, member_update: MemberUpdate) -> MemberResponse:
        """Update member information"""
        try:
            # Check if member exists
            if not MemberModel.get_by_id(member_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Member not found"
                )

            # Check if ID card number is being changed and already exists
            if member_update.id_card_number:
                existing_member = MemberModel.get_by_id_card(member_update.id_card_number)
                if existing_member and existing_member['id'] != member_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="ID card number already exists"
                    )

            # Check if email is being changed and already exists
            if member_update.email:
                existing_email = MemberModel.get_by_email(member_update.email)
                if existing_email and existing_email['id'] != member_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Email already exists"
                    )

            update_data = member_update.dict(exclude_unset=True)
            updated_member = MemberModel.update(member_id, **update_data)

            if not updated_member:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to update member"
                )

            result = MemberResponse(**updated_member).dict()
            return response_success(message="Member updated successfully", data=result)
        except HTTPException as e:
            return response_error(code=e.status_code, message=e.detail)

    @staticmethod
    def delete_member(member_id: int) -> MessageResponse:
        """Delete a member"""
        try:
            # Check if member has active loans
            if MemberModel.has_active_loan(member_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot delete member with active loans"
                )

            success = MemberModel.delete(member_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Member not found"
                )

            return response_success(message="Member deleted successfully")
        except HTTPException as e:
            return response_error(code=e.status_code, message=e.detail)

    @staticmethod
    def get_member_loan_history(member_id: int|str):
        """Get member's loan history"""
        try:
            if not MemberModel.get_by_id(member_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Member not found"
                )

            result = MemberModel.get_loan_history(member_id)
            return response_success(message="Loan history retrieved successfully", data=result)
        except HTTPException as e:
            return response_error(code=e.status_code, message=e.detail)