"""
Books routes for the Library Management System

This module contains all API routes related to book management, including:
- Listing books
- Adding new books
- Retrieving book details
- Updating book information
- Deleting books
- Searching for books
- Managing book categories
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ...database import get_db
from ...crud.book import book_crud
from ...schemas.book import BookResponse, BookCreate, BookUpdate
from ...auth.dependencies import get_current_active_user, get_current_librarian_user, get_current_admin_user
from ...models.user import User
from ...models.book import BookStatus

router = APIRouter()


@router.get("/", response_model=List[BookResponse])
def get_books(
    skip: int = Query(
        0, description="Number of records to skip for pagination"),
    limit: int = Query(100, description="Maximum number of records to return"),
    category: Optional[str] = Query(
        None, description="Filter books by category"),
    status: Optional[BookStatus] = Query(
        None, description="Filter books by status"),
    db: Session = Depends(get_db)
):
    """
    Get all books with optional filtering and pagination

    This endpoint returns a list of books from the library inventory.
    Results can be filtered by category and status, and paginated using skip/limit parameters.

    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **category**: Optional filter by book category
    - **status**: Optional filter by book status (available, loaned, etc.)

    Returns a list of books matching the criteria.
    """
    if category or status:
        books = book_crud.search_books(
            db,
            category=category,
            status=status,
            skip=skip,
            limit=limit
        )
    else:
        books = book_crud.get_multi(db, skip=skip, limit=limit)
    return books


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book_in: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_librarian_user)
):
    """
    Create a new book (librarian/admin only)

    This endpoint allows librarians and administrators to add a new book to the library inventory.

    The request must include all required book information in the request body:
    - ISBN (required)
    - Title (required)
    - Author (required)
    - Other book details (optional)

    Authentication:
    - Requires a valid JWT token
    - User must have librarian or admin role

    Returns the newly created book with its ID and timestamps.
    """
    book = book_crud.create(db, obj_in=book_in)
    return book


@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    """
    Get book by ID

    This endpoint retrieves detailed information about a specific book identified by its ID.

    - **book_id**: The unique identifier of the book

    Returns the book details if found, or a 404 error if the book doesn't exist.
    """
    book = book_crud.get(db, id=book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book
