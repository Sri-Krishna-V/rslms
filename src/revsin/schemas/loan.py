"""
Loan schemas for the Library Management System
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, timedelta
from decimal import Decimal
from ..models.loan import LoanStatus


class LoanBase(BaseModel):
    """Base loan schema"""
    user_id: int = Field(..., gt=0)
    book_id: int = Field(..., gt=0)
    due_date: datetime
    notes: Optional[str] = None


class LoanCreate(LoanBase):
    """Schema for creating a new loan"""
    loan_date: Optional[datetime] = None
    status: LoanStatus = LoanStatus.ACTIVE
    max_renewals: int = Field(default=2, ge=0, le=5)

    @validator('loan_date', always=True)
    def validate_loan_date(cls, v):
        if v is None:
            return datetime.utcnow()
        return v

    @validator('due_date')
    def validate_due_date(cls, v, values):
        loan_date = values.get('loan_date', datetime.utcnow())
        if v <= loan_date:
            raise ValueError('Due date must be after loan date')
        return v


class LoanUpdate(BaseModel):
    """Schema for updating a loan"""
    due_date: Optional[datetime] = None
    return_date: Optional[datetime] = None
    status: Optional[LoanStatus] = None
    fine_amount: Optional[Decimal] = Field(None, ge=0)
    fine_paid: Optional[bool] = None
    notes: Optional[str] = None


class LoanInDB(LoanBase):
    """Schema for loan in database"""
    id: int
    loan_date: datetime
    return_date: Optional[datetime]
    status: LoanStatus
    renewal_count: int
    max_renewals: int
    fine_amount: Decimal
    fine_paid: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LoanResponse(BaseModel):
    """Schema for loan response"""
    id: int
    user_id: int
    book_id: int
    loan_date: datetime
    due_date: datetime
    return_date: Optional[datetime]
    status: LoanStatus
    renewal_count: int
    max_renewals: int
    fine_amount: Decimal
    fine_paid: bool
    notes: Optional[str]
    is_overdue: bool
    days_overdue: int
    can_renew: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LoanWithDetails(LoanResponse):
    """Schema for loan response with user and book details"""
    user: dict  # Will contain user details
    book: dict  # Will contain book details

    class Config:
        from_attributes = True


class LoanRenewal(BaseModel):
    """Schema for loan renewal"""
    new_due_date: Optional[datetime] = None

    @validator('new_due_date', always=True)
    def validate_new_due_date(cls, v):
        if v is None:
            # Default to 14 days from now
            return datetime.utcnow() + timedelta(days=14)
        if v <= datetime.utcnow():
            raise ValueError('New due date must be in the future')
        return v


class LoanReturn(BaseModel):
    """Schema for loan return"""
    return_date: Optional[datetime] = None
    fine_amount: Optional[Decimal] = Field(None, ge=0)
    fine_paid: bool = False
    notes: Optional[str] = None

    @validator('return_date', always=True)
    def validate_return_date(cls, v):
        if v is None:
            return datetime.utcnow()
        return v


class LoanSearch(BaseModel):
    """Schema for loan search"""
    user_id: Optional[int] = Field(None, gt=0)
    book_id: Optional[int] = Field(None, gt=0)
    status: Optional[LoanStatus] = None
    overdue_only: bool = False
    active_only: bool = False
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)
