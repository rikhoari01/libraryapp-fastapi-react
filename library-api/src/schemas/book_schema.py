from pydantic import BaseModel, validator
from typing import Optional

class BookCreate(BaseModel):
    title: str
    isbn: str
    stock: int = 0

    @validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

    @validator('isbn')
    def validate_isbn(cls, v):
        isbn_clean = v.replace('-', '').replace(' ', '')
        if len(isbn_clean) < 10:
            raise ValueError('ISBN must be at least 10 characters long')
        return isbn_clean

    @validator('stock')
    def validate_stock(cls, v):
        if v < 0:
            raise ValueError('Stock cannot be negative')
        return v


class BookUpdate(BaseModel):
    title: Optional[str] = None
    isbn: Optional[str] = None
    stock: Optional[int] = None

    @validator('title')
    def validate_title(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip() if v else v

    @validator('isbn')
    def validate_isbn(cls, v):
        if v is not None:
            isbn_clean = v.replace('-', '').replace(' ', '')
            if len(isbn_clean) < 10:
                raise ValueError('ISBN must be at least 10 characters long')
            return isbn_clean
        return v

    @validator('stock')
    def validate_stock(cls, v):
        if v is not None and v < 0:
            raise ValueError('Stock cannot be negative')
        return v


class BookResponse(BaseModel):
    id: int
    title: str
    isbn: str
    stock: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class BookStockUpdate(BaseModel):
    stock: int

    @validator('stock')
    def validate_stock(cls, v):
        if v < 0:
            raise ValueError('Stock cannot be negative')
        return v