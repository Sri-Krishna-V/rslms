"""
Book model for library management system

This module defines the Book model which represents books in the library inventory.
It includes all book metadata, status tracking, and inventory management fields.
"""

from sqlalchemy import Column, String, Integer, Text, Boolean, Enum as SQLEnum, Numeric
from sqlalchemy.orm import relationship
from enum import Enum
from .base import Base


class BookStatus(str, Enum):
    """
    Book status in the library

    Defines the possible states a book can be in:
    - AVAILABLE: Book is available for borrowing
    - LOANED: Book is currently on loan to a member
    - RESERVED: Book is reserved for pickup
    - MAINTENANCE: Book is undergoing repair or maintenance
    - LOST: Book has been reported lost
    """
    AVAILABLE = "available"
    LOANED = "loaned"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"
    LOST = "lost"


class Book(Base):
    """
    Book model for library inventory

    This model stores all information about books in the library collection,
    including bibliographic data, inventory status, and physical location.

    Relationships:
    - loans: One-to-many relationship with Loan model

    Properties:
    - is_available: Boolean indicating if the book can be borrowed
    """

    __tablename__ = "books"

    # Book identification
    isbn = Column(String, unique=True, index=True, nullable=False,
                  comment="International Standard Book Number, unique identifier")
    title = Column(String, nullable=False, index=True,
                   comment="Book title")
    author = Column(String, nullable=False, index=True,
                    comment="Book author(s)")
    publisher = Column(String, nullable=True,
                       comment="Publishing company")
    publication_year = Column(Integer, nullable=True,
                              comment="Year of publication")
    edition = Column(String, nullable=True,
                     comment="Edition information (e.g., '2nd Edition')")

    # Book details
    description = Column(Text, nullable=True,
                         comment="Book summary or description")
    category = Column(String, nullable=True, index=True,
                      comment="Book category or genre")
    language = Column(String, default="English",
                      comment="Language the book is written in")
    pages = Column(Integer, nullable=True,
                   comment="Number of pages")

    # Library management
    status = Column(SQLEnum(BookStatus),
                    default=BookStatus.AVAILABLE, index=True,
                    comment="Current status of the book")
    location = Column(String, nullable=True,
                      comment="Physical location in the library (shelf/section)")
    quantity = Column(Integer, default=1,
                      comment="Total number of copies owned by the library")
    available_quantity = Column(Integer, default=1,
                                comment="Number of copies currently available for loan")

    # Pricing (if applicable)
    price = Column(Numeric(10, 2), nullable=True,
                   comment="Purchase price or replacement value")

    # Relationships
    loans = relationship("Loan", back_populates="book")

    @property
    def is_available(self):
        """
        Check if the book is available for borrowing

        Returns:
            bool: True if the book is available and has copies that can be borrowed
        """
        return self.status == BookStatus.AVAILABLE and self.available_quantity > 0

    def __repr__(self):
        """String representation of the Book object"""
        return f"<Book(id={self.id}, isbn='{self.isbn}', title='{self.title}', status='{self.status}')>"
