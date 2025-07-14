"""
Book schemas for the Library Management System
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from decimal import Decimal
from ..models.book import BookStatus


class BookBase(BaseModel):
    """Base book schema"""
    isbn: str = Field(..., min_length=10, max_length=17)
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    publisher: Optional[str] = Field(None, max_length=255)
    publication_year: Optional[int] = Field(None, ge=1000, le=2025)
    edition: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    language: str = Field(default="English", max_length=50)
    pages: Optional[int] = Field(None, ge=1)
    location: Optional[str] = Field(None, max_length=100)
    quantity: int = Field(default=1, ge=1)
    price: Optional[Decimal] = Field(None, ge=0)

    @validator('isbn')
    def validate_isbn(cls, v):
        # Remove hyphens and spaces
        isbn = v.replace('-', '').replace(' ', '')
        if len(isbn) not in [10, 13]:
            raise ValueError('ISBN must be 10 or 13 digits')
        if not isbn.isdigit():
            raise ValueError('ISBN must contain only digits')
        return isbn


class BookCreate(BookBase):
    """Schema for creating a new book"""
    status: BookStatus = BookStatus.AVAILABLE
    available_quantity: Optional[int] = None

    @validator('available_quantity', always=True)
    def validate_available_quantity(cls, v, values):
        if v is None:
            return values.get('quantity', 1)
        if v > values.get('quantity', 1):
            raise ValueError('Available quantity cannot exceed total quantity')
        return v


class BookUpdate(BaseModel):
    """Schema for updating a book"""
    isbn: Optional[str] = Field(None, min_length=10, max_length=17)
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    publisher: Optional[str] = Field(None, max_length=255)
    publication_year: Optional[int] = Field(None, ge=1000, le=2025)
    edition: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    language: Optional[str] = Field(None, max_length=50)
    pages: Optional[int] = Field(None, ge=1)
    status: Optional[BookStatus] = None
    location: Optional[str] = Field(None, max_length=100)
    quantity: Optional[int] = Field(None, ge=1)
    available_quantity: Optional[int] = Field(None, ge=0)
    price: Optional[Decimal] = Field(None, ge=0)

    @validator('isbn')
    def validate_isbn(cls, v):
        if v is not None:
            # Remove hyphens and spaces
            isbn = v.replace('-', '').replace(' ', '')
            if len(isbn) not in [10, 13]:
                raise ValueError('ISBN must be 10 or 13 digits')
            if not isbn.isdigit():
                raise ValueError('ISBN must contain only digits')
            return isbn
        return v


class BookInDB(BookBase):
    """Schema for book in database"""
    id: int
    status: BookStatus
    available_quantity: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BookResponse(BaseModel):
    """Schema for book response"""
    id: int
    isbn: str
    title: str
    author: str
    publisher: Optional[str]
    publication_year: Optional[int]
    edition: Optional[str]
    description: Optional[str]
    category: Optional[str]
    language: str
    pages: Optional[int]
    status: BookStatus
    location: Optional[str]
    quantity: int
    available_quantity: int
    price: Optional[Decimal]
    is_available: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BookSearch(BaseModel):
    """Schema for book search"""
    query: Optional[str] = None
    category: Optional[str] = None
    author: Optional[str] = None
    status: Optional[BookStatus] = None
    available_only: bool = False
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)
