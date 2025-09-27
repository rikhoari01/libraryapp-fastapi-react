from pydantic import BaseModel, validator
from typing import Optional
from datetime import date

class LoanCreate(BaseModel):
    member_id: int
    book_id: int
    return_deadline: date

    @validator('member_id')
    def validate_member_id(cls, v):
        if v <= 0:
            raise ValueError('Member ID must be positive')
        return v

    @validator('book_id')
    def validate_book_id(cls, v):
        if v <= 0:
            raise ValueError('Book ID must be positive')
        return v

    @validator('return_deadline')
    def validate_return_deadline(cls, v):
        if v <= date.today():
            raise ValueError('Return deadline must be in the future')
        if (v - date.today()).days > 30:
            raise ValueError('Loan duration cannot exceed 30 days')
        return v


class LoanResponse(BaseModel):
    id: int
    member_id: int
    book_id: int
    loan_date: str
    return_deadline: str
    actual_return_date: Optional[str] = None
    status: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class LoanDetailResponse(BaseModel):
    id: int
    member_id: int
    member_name: str
    member_id_card: str
    book_id: int
    book_title: str
    book_isbn: str
    loan_date: str
    return_deadline: str
    actual_return_date: Optional[str] = None
    status: str
    return_status: str
    days_difference: Optional[int] = None

    class Config:
        from_attributes = True


class LoanReturnResponse(BaseModel):
    book_id: int
    card_member_id: str
    return_date: str
    was_late: bool
    days_late: Optional[int] = None

    class Config:
        from_attributes = True


# Common response schemas
class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None


class StatsResponse(BaseModel):
    total_books: int
    total_stock: int
    total_members: int
    active_loans: int
    overdue_loans: int
    total_loans_ever: int
    books_available: int