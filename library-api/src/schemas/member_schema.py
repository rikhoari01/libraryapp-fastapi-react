from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class MemberCreate(BaseModel):
    id_card_number: str
    name: str
    email: EmailStr

    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        if len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip()

    @validator('id_card_number')
    def validate_id_card(cls, v):
        if not v.strip():
            raise ValueError('ID card number cannot be empty')
        if len(v.strip()) < 3:
            raise ValueError('ID card number must be at least 3 characters long')
        return v.strip()


class MemberUpdate(BaseModel):
    id_card_number: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None

    @validator('name')
    def validate_name(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('Name cannot be empty')
            if len(v.strip()) < 2:
                raise ValueError('Name must be at least 2 characters long')
            return v.strip()
        return v

    @validator('id_card_number')
    def validate_id_card(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('ID card number cannot be empty')
            if len(v.strip()) < 3:
                raise ValueError('ID card number must be at least 3 characters long')
            return v.strip()
        return v


class MemberResponse(BaseModel):
    id: int
    id_card_number: str
    name: str
    email: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class MemberWithLoansResponse(BaseModel):
    id: int
    id_card_number: str
    name: str
    email: str
    created_at: str
    updated_at: str
    has_active_loan: bool
    total_loans: int

    class Config:
        from_attributes = True