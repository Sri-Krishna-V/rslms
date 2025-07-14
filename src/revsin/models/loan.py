"""
Loan model for library management system

This module defines the Loan model which represents book borrowing transactions.
It tracks loan status, due dates, renewals, and fine calculations for overdue books.
"""

from sqlalchemy import Column, Integer, DateTime, Boolean, Enum as SQLEnum, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from enum import Enum
from datetime import datetime, timedelta
from .base import Base


class LoanStatus(str, Enum):
    """
    Loan status in the library

    Defines the possible states a loan can be in:
    - ACTIVE: Book is currently borrowed and not yet returned
    - RETURNED: Book has been returned to the library
    - OVERDUE: Book is past its due date and not returned
    - RENEWED: Loan period has been extended
    - LOST: Book has been reported lost during the loan period
    """
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"
    RENEWED = "renewed"
    LOST = "lost"


class Loan(Base):
    """
    Loan model for tracking book loans

    This model represents a transaction where a user borrows a book from the library.
    It tracks all aspects of the loan lifecycle including due dates, returns, renewals,
    and fine calculations for overdue books.

    Relationships:
    - user: Many-to-one relationship with User model
    - book: Many-to-one relationship with Book model

    Properties:
    - is_overdue: Boolean indicating if the loan is past due date
    - days_overdue: Number of days the loan is overdue
    - can_renew: Boolean indicating if the loan can be renewed
    """

    __tablename__ = "loans"

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False,
                     comment="ID of the user who borrowed the book")
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False,
                     comment="ID of the borrowed book")

    # Loan details
    loan_date = Column(DateTime, default=datetime.utcnow,
                       comment="Date and time when the book was borrowed")
    due_date = Column(DateTime, nullable=False,
                      comment="Date by which the book must be returned")
    return_date = Column(DateTime, nullable=True,
                         comment="Date and time when the book was returned (null if not returned)")

    # Loan management
    status = Column(SQLEnum(LoanStatus), default=LoanStatus.ACTIVE, index=True,
                    comment="Current status of the loan (active, returned, overdue, etc.)")
    renewal_count = Column(Integer, default=0,
                           comment="Number of times this loan has been renewed")
    max_renewals = Column(Integer, default=2,
                          comment="Maximum number of renewals allowed for this loan")

    # Fine management
    fine_amount = Column(Numeric(10, 2), default=0.0,
                         comment="Amount of fine for overdue return (in currency units)")
    fine_paid = Column(Boolean, default=False,
                       comment="Whether the fine has been paid")

    # Notes
    notes = Column(Text, nullable=True,
                   comment="Additional notes about the loan (condition of book, etc.)")

    # Relationships
    user = relationship("User", back_populates="loans")
    book = relationship("Book", back_populates="loans")

    @property
    def is_overdue(self):
        """
        Check if the loan is overdue

        A loan is considered overdue if the current date is past the due date
        and the loan is still active (not returned).

        Returns:
            bool: True if the loan is overdue, False otherwise
        """
        return datetime.utcnow() > self.due_date and self.status == LoanStatus.ACTIVE

    @property
    def days_overdue(self):
        """
        Calculate the number of days the loan is overdue

        Returns:
            int: Number of days overdue, or 0 if not overdue
        """
        if self.is_overdue:
            return (datetime.utcnow() - self.due_date).days
        return 0

    @property
    def can_renew(self):
        """
        Check if the loan can be renewed

        A loan can be renewed if:
        1. The renewal count is less than the maximum allowed renewals
        2. The loan is active (not returned)
        3. The loan is not overdue

        Returns:
            bool: True if the loan can be renewed, False otherwise
        """
        return (self.renewal_count < self.max_renewals and
                self.status == LoanStatus.ACTIVE and
                not self.is_overdue)

    def calculate_fine(self, daily_fine_rate=0.50):
        """
        Calculate fine for overdue books

        Calculates the fine amount based on the number of days overdue
        and the daily fine rate.

        Args:
            daily_fine_rate (float): Amount to charge per day overdue (default: 0.50)

        Returns:
            float: Total fine amount
        """
        if self.is_overdue:
            return self.days_overdue * daily_fine_rate
        return 0.0

    def __repr__(self):
        """String representation of the Loan object"""
        return f"<Loan(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, status='{self.status}')>"
