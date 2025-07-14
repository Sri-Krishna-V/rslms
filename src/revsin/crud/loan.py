"""
Loan CRUD operations for the Library Management System
"""

from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from datetime import datetime, timedelta

from .base import CRUDBase
from ..models.loan import Loan, LoanStatus
from ..models.book import BookStatus
from ..schemas.loan import LoanCreate, LoanUpdate
from ..database.redis_client import cache, get_user_loans_cache_key, get_overdue_loans_cache_key


class CRUDLoan(CRUDBase[Loan, LoanCreate, LoanUpdate]):
    """CRUD operations for Loan model"""

    def create_loan(self, db: Session, *, obj_in: LoanCreate) -> Optional[Loan]:
        """Create a new loan with book availability check"""
        from .book import book_crud

        # Check if book is available
        book = book_crud.get(db, obj_in.book_id)
        if not book or not book.is_available:
            return None

        # Update book availability
        updated_book = book_crud.update_availability(
            db, book_id=obj_in.book_id, quantity_change=-1)
        if not updated_book:
            return None

        # Create the loan
        loan = super().create(db, obj_in=obj_in)

        # Invalidate cache
        cache.delete(get_user_loans_cache_key(loan.user_id))
        cache.delete_pattern("loans:*")

        return loan

    def return_book(self, db: Session, *, loan_id: int, return_data: dict) -> Optional[Loan]:
        """Return a book and update loan status"""
        from .book import book_crud

        loan = self.get(db, loan_id)
        if not loan or loan.status != LoanStatus.ACTIVE:
            return None

        # Update loan
        return_date = return_data.get("return_date", datetime.utcnow())
        fine_amount = return_data.get("fine_amount", 0.0)

        # Calculate fine if overdue
        if loan.is_overdue:
            fine_amount = max(fine_amount, loan.calculate_fine())

        update_data = {
            "return_date": return_date,
            "status": LoanStatus.RETURNED,
            "fine_amount": fine_amount,
            "fine_paid": return_data.get("fine_paid", False),
            "notes": return_data.get("notes")
        }

        updated_loan = super().update(db, db_obj=loan, obj_in=update_data)

        # Update book availability
        book_crud.update_availability(
            db, book_id=loan.book_id, quantity_change=1)

        # Invalidate cache
        cache.delete(get_user_loans_cache_key(loan.user_id))
        cache.delete_pattern("loans:*")

        return updated_loan

    def renew_loan(self, db: Session, *, loan_id: int, new_due_date: datetime) -> Optional[Loan]:
        """Renew a loan"""
        loan = self.get(db, loan_id)
        if not loan or not loan.can_renew:
            return None

        update_data = {
            "due_date": new_due_date,
            "renewal_count": loan.renewal_count + 1,
            "status": LoanStatus.RENEWED
        }

        updated_loan = super().update(db, db_obj=loan, obj_in=update_data)

        # Invalidate cache
        cache.delete(get_user_loans_cache_key(loan.user_id))
        cache.delete_pattern("loans:*")

        return updated_loan

    def get_user_loans(
        self,
        db: Session,
        *,
        user_id: int,
        active_only: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[Loan]:
        """Get loans for a specific user"""
        # Try cache first for active loans
        if active_only and skip == 0 and limit == 100:
            cache_key = get_user_loans_cache_key(user_id)
            cached_loans = cache.get(cache_key)
            if cached_loans:
                return [Loan(**loan) for loan in cached_loans]

        # Query database
        query = db.query(Loan).filter(Loan.user_id == user_id)

        if active_only:
            query = query.filter(Loan.status == LoanStatus.ACTIVE)

        loans = query.offset(skip).limit(limit).all()

        # Cache active loans
        if active_only and skip == 0 and limit == 100 and loans:
            loans_dict = []
            for loan in loans:
                loan_dict = {
                    "id": loan.id,
                    "user_id": loan.user_id,
                    "book_id": loan.book_id,
                    "loan_date": loan.loan_date.isoformat(),
                    "due_date": loan.due_date.isoformat(),
                    "return_date": loan.return_date.isoformat() if loan.return_date else None,
                    "status": loan.status.value,
                    "renewal_count": loan.renewal_count,
                    "max_renewals": loan.max_renewals,
                    "fine_amount": str(loan.fine_amount),
                    "fine_paid": loan.fine_paid,
                    "notes": loan.notes,
                    "created_at": loan.created_at.isoformat(),
                    "updated_at": loan.updated_at.isoformat()
                }
                loans_dict.append(loan_dict)
            cache.set(cache_key, loans_dict)

        return loans

    def get_book_loans(
        self,
        db: Session,
        *,
        book_id: int,
        active_only: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[Loan]:
        """Get loans for a specific book"""
        query = db.query(Loan).filter(Loan.book_id == book_id)

        if active_only:
            query = query.filter(Loan.status == LoanStatus.ACTIVE)

        return query.offset(skip).limit(limit).all()

    def get_overdue_loans(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Loan]:
        """Get overdue loans"""
        # Try cache first
        if skip == 0 and limit == 100:
            cache_key = get_overdue_loans_cache_key()
            cached_loans = cache.get(cache_key)
            if cached_loans:
                return [Loan(**loan) for loan in cached_loans]

        # Query database
        current_time = datetime.utcnow()
        loans = (
            db.query(Loan)
            .filter(
                and_(
                    Loan.status == LoanStatus.ACTIVE,
                    Loan.due_date < current_time
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

        # Cache the result
        if skip == 0 and limit == 100 and loans:
            loans_dict = []
            for loan in loans:
                loan_dict = {
                    "id": loan.id,
                    "user_id": loan.user_id,
                    "book_id": loan.book_id,
                    "loan_date": loan.loan_date.isoformat(),
                    "due_date": loan.due_date.isoformat(),
                    "return_date": loan.return_date.isoformat() if loan.return_date else None,
                    "status": loan.status.value,
                    "renewal_count": loan.renewal_count,
                    "max_renewals": loan.max_renewals,
                    "fine_amount": str(loan.fine_amount),
                    "fine_paid": loan.fine_paid,
                    "notes": loan.notes,
                    "created_at": loan.created_at.isoformat(),
                    "updated_at": loan.updated_at.isoformat()
                }
                loans_dict.append(loan_dict)
            cache.set(cache_key, loans_dict, expire=180)  # Cache for 3 minutes

        return loans

    def get_loans_with_details(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[Loan]:
        """Get loans with user and book details"""
        return (
            db.query(Loan)
            .options(
                joinedload(Loan.user),
                joinedload(Loan.book)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search_loans(
        self,
        db: Session,
        *,
        user_id: Optional[int] = None,
        book_id: Optional[int] = None,
        status: Optional[LoanStatus] = None,
        overdue_only: bool = False,
        active_only: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[Loan]:
        """Search loans with multiple criteria"""
        query = db.query(Loan)

        if user_id:
            query = query.filter(Loan.user_id == user_id)

        if book_id:
            query = query.filter(Loan.book_id == book_id)

        if status:
            query = query.filter(Loan.status == status)

        if active_only:
            query = query.filter(Loan.status == LoanStatus.ACTIVE)

        if overdue_only:
            current_time = datetime.utcnow()
            query = query.filter(
                and_(
                    Loan.status == LoanStatus.ACTIVE,
                    Loan.due_date < current_time
                )
            )

        return query.offset(skip).limit(limit).all()

    def get_loan_statistics(self, db: Session) -> dict:
        """Get loan statistics"""
        # Try cache first
        cache_key = "loans:statistics"
        cached_stats = cache.get(cache_key)
        if cached_stats:
            return cached_stats

        # Query database
        current_time = datetime.utcnow()

        total_loans = db.query(Loan).count()
        active_loans = db.query(Loan).filter(
            Loan.status == LoanStatus.ACTIVE).count()
        overdue_loans = db.query(Loan).filter(
            and_(
                Loan.status == LoanStatus.ACTIVE,
                Loan.due_date < current_time
            )
        ).count()
        returned_loans = db.query(Loan).filter(
            Loan.status == LoanStatus.RETURNED).count()

        stats = {
            "total_loans": total_loans,
            "active_loans": active_loans,
            "overdue_loans": overdue_loans,
            "returned_loans": returned_loans
        }

        # Cache the result
        cache.set(cache_key, stats, expire=300)  # Cache for 5 minutes

        return stats

    def update_overdue_loans(self, db: Session) -> int:
        """Update overdue loan statuses"""
        current_time = datetime.utcnow()

        # Find overdue loans
        overdue_loans = db.query(Loan).filter(
            and_(
                Loan.status == LoanStatus.ACTIVE,
                Loan.due_date < current_time
            )
        ).all()

        count = 0
        for loan in overdue_loans:
            loan.status = LoanStatus.OVERDUE
            loan.fine_amount = loan.calculate_fine()
            count += 1

        if count > 0:
            db.commit()
            # Invalidate cache
            cache.delete_pattern("loans:*")

        return count


loan_crud = CRUDLoan(Loan)
