"""
CRUD operations for the Library Management System
"""

from .base import CRUDBase
from .user import user_crud
from .book import book_crud
from .loan import loan_crud

__all__ = ["CRUDBase", "user_crud", "book_crud", "loan_crud"]
