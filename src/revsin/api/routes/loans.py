"""
Loans routes for the Library Management System
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...database import get_db
from ...crud.loan import loan_crud
from ...schemas.loan import LoanResponse, LoanCreate, LoanReturn
from ...auth.dependencies import get_current_active_user, get_current_librarian_user
from ...models.user import User

router = APIRouter()


@router.get("/", response_model=List[LoanResponse])
def get_loans(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_librarian_user)
):
    """
    Get all loans (librarian/admin only)
    """
    loans = loan_crud.get_multi(db, skip=skip, limit=limit)
    return loans


@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def create_loan(
    loan_in: LoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new loan
    """
    loan = loan_crud.create_loan(db, obj_in=loan_in)
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book not available or loan creation failed"
        )
    return loan


@router.get("/{loan_id}", response_model=LoanResponse)
def get_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get loan by ID
    """
    loan = loan_crud.get(db, id=loan_id)
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found"
        )
    return loan
