"""
Book CRUD operations for the Library Management System
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from .base import CRUDBase
from ..models.book import Book, BookStatus
from ..schemas.book import BookCreate, BookUpdate
from ..database.redis_client import cache, get_book_cache_key, get_books_list_cache_key


class CRUDBook(CRUDBase[Book, BookCreate, BookUpdate]):
    """CRUD operations for Book model"""

    def get(self, db: Session, id: int) -> Optional[Book]:
        """Get book by ID with caching"""
        # Try cache first
        cache_key = get_book_cache_key(id)
        cached_book = cache.get(cache_key)
        if cached_book:
            return Book(**cached_book)

        # Query database
        book = super().get(db, id)
        if book:
            # Cache the result
            book_dict = {
                "id": book.id,
                "isbn": book.isbn,
                "title": book.title,
                "author": book.author,
                "publisher": book.publisher,
                "publication_year": book.publication_year,
                "edition": book.edition,
                "description": book.description,
                "category": book.category,
                "language": book.language,
                "pages": book.pages,
                "status": book.status.value,
                "location": book.location,
                "quantity": book.quantity,
                "available_quantity": book.available_quantity,
                "price": str(book.price) if book.price else None,
                "created_at": book.created_at.isoformat(),
                "updated_at": book.updated_at.isoformat()
            }
            cache.set(cache_key, book_dict)

        return book

    def get_by_isbn(self, db: Session, *, isbn: str) -> Optional[Book]:
        """Get book by ISBN"""
        # Try cache first
        cache_key = f"book:isbn:{isbn}"
        cached_book = cache.get(cache_key)
        if cached_book:
            return Book(**cached_book)

        # Query database
        book = db.query(Book).filter(Book.isbn == isbn).first()
        if book:
            # Cache the result
            book_dict = {
                "id": book.id,
                "isbn": book.isbn,
                "title": book.title,
                "author": book.author,
                "publisher": book.publisher,
                "publication_year": book.publication_year,
                "edition": book.edition,
                "description": book.description,
                "category": book.category,
                "language": book.language,
                "pages": book.pages,
                "status": book.status.value,
                "location": book.location,
                "quantity": book.quantity,
                "available_quantity": book.available_quantity,
                "price": str(book.price) if book.price else None,
                "created_at": book.created_at.isoformat(),
                "updated_at": book.updated_at.isoformat()
            }
            cache.set(cache_key, book_dict)
            cache.set(get_book_cache_key(book.id), book_dict)

        return book

    def create(self, db: Session, *, obj_in: BookCreate) -> Book:
        """Create a new book"""
        obj_in_data = obj_in.dict()
        db_obj = Book(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # Cache the new book
        book_dict = {
            "id": db_obj.id,
            "isbn": db_obj.isbn,
            "title": db_obj.title,
            "author": db_obj.author,
            "publisher": db_obj.publisher,
            "publication_year": db_obj.publication_year,
            "edition": db_obj.edition,
            "description": db_obj.description,
            "category": db_obj.category,
            "language": db_obj.language,
            "pages": db_obj.pages,
            "status": db_obj.status.value,
            "location": db_obj.location,
            "quantity": db_obj.quantity,
            "available_quantity": db_obj.available_quantity,
            "price": str(db_obj.price) if db_obj.price else None,
            "created_at": db_obj.created_at.isoformat(),
            "updated_at": db_obj.updated_at.isoformat()
        }
        cache.set(get_book_cache_key(db_obj.id), book_dict)
        cache.set(f"book:isbn:{db_obj.isbn}", book_dict)

        # Invalidate books list cache
        cache.delete_pattern("books:list:*")

        return db_obj

    def update(self, db: Session, *, db_obj: Book, obj_in: BookUpdate) -> Book:
        """Update book"""
        updated_book = super().update(db, db_obj=db_obj, obj_in=obj_in)

        # Invalidate cache
        cache.delete(get_book_cache_key(updated_book.id))
        cache.delete(f"book:isbn:{updated_book.isbn}")
        cache.delete_pattern("books:list:*")

        return updated_book

    def search_books(
        self,
        db: Session,
        *,
        query: Optional[str] = None,
        category: Optional[str] = None,
        author: Optional[str] = None,
        status: Optional[BookStatus] = None,
        available_only: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[Book]:
        """Search books with multiple criteria"""
        db_query = db.query(Book)

        # Apply filters
        if query:
            db_query = db_query.filter(
                or_(
                    Book.title.ilike(f"%{query}%"),
                    Book.author.ilike(f"%{query}%"),
                    Book.isbn.ilike(f"%{query}%"),
                    Book.publisher.ilike(f"%{query}%"),
                    Book.description.ilike(f"%{query}%")
                )
            )

        if category:
            db_query = db_query.filter(Book.category.ilike(f"%{category}%"))

        if author:
            db_query = db_query.filter(Book.author.ilike(f"%{author}%"))

        if status:
            db_query = db_query.filter(Book.status == status)

        if available_only:
            db_query = db_query.filter(
                and_(
                    Book.status == BookStatus.AVAILABLE,
                    Book.available_quantity > 0
                )
            )

        return db_query.offset(skip).limit(limit).all()

    def get_available_books(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Book]:
        """Get available books"""
        return (
            db.query(Book)
            .filter(
                and_(
                    Book.status == BookStatus.AVAILABLE,
                    Book.available_quantity > 0
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_books_by_category(
        self,
        db: Session,
        *,
        category: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Book]:
        """Get books by category with caching"""
        # Try cache first
        cache_key = get_books_list_cache_key(skip, limit, category)
        cached_books = cache.get(cache_key)
        if cached_books:
            return [Book(**book) for book in cached_books]

        # Query database
        books = (
            db.query(Book)
            .filter(Book.category.ilike(f"%{category}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

        # Cache the result
        if books:
            books_dict = []
            for book in books:
                book_dict = {
                    "id": book.id,
                    "isbn": book.isbn,
                    "title": book.title,
                    "author": book.author,
                    "publisher": book.publisher,
                    "publication_year": book.publication_year,
                    "edition": book.edition,
                    "description": book.description,
                    "category": book.category,
                    "language": book.language,
                    "pages": book.pages,
                    "status": book.status.value,
                    "location": book.location,
                    "quantity": book.quantity,
                    "available_quantity": book.available_quantity,
                    "price": str(book.price) if book.price else None,
                    "created_at": book.created_at.isoformat(),
                    "updated_at": book.updated_at.isoformat()
                }
                books_dict.append(book_dict)
            cache.set(cache_key, books_dict)

        return books

    def get_books_by_author(
        self,
        db: Session,
        *,
        author: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Book]:
        """Get books by author"""
        return (
            db.query(Book)
            .filter(Book.author.ilike(f"%{author}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_availability(self, db: Session, *, book_id: int, quantity_change: int) -> Optional[Book]:
        """Update book availability (for loans/returns)"""
        book = self.get(db, book_id)
        if not book:
            return None

        new_available_quantity = book.available_quantity + quantity_change

        if new_available_quantity < 0:
            return None  # Cannot have negative availability

        if new_available_quantity > book.quantity:
            return None  # Cannot have more available than total quantity

        # Update availability
        book.available_quantity = new_available_quantity

        # Update status based on availability
        if new_available_quantity == 0:
            book.status = BookStatus.LOANED
        elif book.status == BookStatus.LOANED and new_available_quantity > 0:
            book.status = BookStatus.AVAILABLE

        db.commit()
        db.refresh(book)

        # Invalidate cache
        cache.delete(get_book_cache_key(book.id))
        cache.delete(f"book:isbn:{book.isbn}")
        cache.delete_pattern("books:list:*")

        return book

    def get_categories(self, db: Session) -> List[str]:
        """Get all unique categories"""
        # Try cache first
        cache_key = "books:categories"
        cached_categories = cache.get(cache_key)
        if cached_categories:
            return cached_categories

        # Query database
        categories = db.query(Book.category).distinct().filter(
            Book.category.isnot(None)).all()
        categories_list = [cat[0] for cat in categories if cat[0]]

        # Cache the result
        # Cache for 10 minutes
        cache.set(cache_key, categories_list, expire=600)

        return categories_list


book_crud = CRUDBook(Book)
