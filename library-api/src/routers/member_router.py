from fastapi import APIRouter, status, Depends
from typing import List
from controllers.member_controller import MemberController
from schemas.member_schema import MemberCreate, MemberUpdate, MemberResponse
from schemas.loan_schema import MessageResponse
from middleware.auth import verify_credentials

router = APIRouter(
    prefix="/members",
    tags=["Members"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(verify_credentials)],
)


@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
async def create_member(member: MemberCreate):
    """
    Create a new member

    - **id_card_number**: Unique ID card number (required)
    - **name**: Member's full name (required, minimum 2 characters)
    - **email**: Valid email address (required, unique)
    """
    return MemberController.create_member(member)


@router.get("/", response_model=List[MemberResponse])
async def get_members(skip: int = 0, limit: int = 100):
    """
    Get all members with pagination

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    return MemberController.get_members(skip=skip, limit=limit)


@router.get("/{member_id}", response_model=MemberResponse)
async def get_member(member_id: int):
    """
    Get a specific member by ID

    - **member_id**: The ID of the member to retrieve
    """
    return MemberController.get_member_by_id(member_id)


@router.get("/id-card/{id_card_number}", response_model=MemberResponse)
async def get_member_by_id_card(id_card_number: str):
    """
    Get a member by ID card number

    - **id_card_number**: The ID card number of the member to retrieve
    """
    return MemberController.get_member_by_id_card(id_card_number)


@router.put("/{member_id}", response_model=MemberResponse)
async def update_member(member_id: int, member_update: MemberUpdate):
    """
    Update member information

    - **member_id**: The ID of the member to update
    - **id_card_number**: New ID card number (optional)
    - **name**: New name (optional)
    - **email**: New email address (optional)
    """
    return MemberController.update_member(member_id, member_update)


@router.delete("/{member_id}", response_model=MessageResponse)
async def delete_member(member_id: int):
    """
    Delete a member

    - **member_id**: The ID of the member to delete

    Note: Cannot delete members with active loans
    """
    return MemberController.delete_member(member_id)


@router.get("/{member_id}/loan-history")
async def get_member_loan_history(member_id: int):
    """
    Get member's loan history

    - **member_id**: The ID of the member
    """
    return MemberController.get_member_loan_history(member_id)