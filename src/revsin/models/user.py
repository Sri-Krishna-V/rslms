"""
User model for library management system
"""

from sqlalchemy import Column, String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from .base import Base


class UserRole(str, Enum):
    """User roles in the library system"""
    ADMIN = "admin"
    LIBRARIAN = "librarian"
    MEMBER = "member"


class User(Base):
    """User model for library members and staff"""

    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(SQLEnum(UserRole), default=UserRole.MEMBER)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)

    # Relationships
    loans = relationship("Loan", back_populates="user")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
