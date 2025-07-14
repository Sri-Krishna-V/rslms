"""
Base CRUD operations for the Library Management System

This module provides a generic base class for CRUD (Create, Read, Update, Delete)
operations that can be used with any SQLAlchemy model. It implements common database
operations with type safety using generics.

The CRUDBase class is designed to be extended for specific models, providing
a consistent interface for database operations across the application.
"""

from typing import Generic, TypeVar, Type, Optional, List, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from ..models.base import Base

# Type variables for generic typing
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for CRUD operations

    This generic class provides standard Create, Read, Update, Delete operations
    for SQLAlchemy models. It uses Pydantic models for input validation when
    creating and updating records.

    Type Parameters:
    - ModelType: SQLAlchemy model class
    - CreateSchemaType: Pydantic model for create operations
    - UpdateSchemaType: Pydantic model for update operations

    Usage example:
    ```python
    from .models.user import User
    from .schemas.user import UserCreate, UserUpdate

    class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
        # Add user-specific methods here
        pass

    user_crud = CRUDUser(User)
    ```
    """

    def __init__(self, model: Type[ModelType]):
        """
        Initialize the CRUD object with a SQLAlchemy model class

        Args:
            model: A SQLAlchemy model class that inherits from Base
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Get a single record by ID

        Args:
            db: SQLAlchemy database session
            id: Primary key ID value

        Returns:
            Model instance if found, None otherwise

        Example:
            ```python
            user = user_crud.get(db, id=1)
            ```
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ModelType]:
        """
        Get multiple records with optional filtering and pagination

        Args:
            db: SQLAlchemy database session
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            filters: Optional dictionary of field-value pairs for filtering
                     Only exact matches are supported

        Returns:
            List of model instances matching the criteria

        Example:
            ```python
            # Get all active users
            active_users = user_crud.get_multi(db, filters={"is_active": True})

            # Get users with pagination
            users_page = user_crud.get_multi(db, skip=20, limit=10)
            ```
        """
        query = db.query(self.model)

        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)

        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record

        Args:
            db: SQLAlchemy database session
            obj_in: Pydantic model with the data for the new record

        Returns:
            Created model instance with ID and timestamps

        Example:
            ```python
            new_user = UserCreate(
                email="user@example.com",
                username="newuser",
                password="secret"
            )
            user = user_crud.create(db, obj_in=new_user)
            ```

        Note:
            The create schema should include all required fields for the model.
            The password field, if present, will typically be hashed in the
            model-specific CRUD implementation.
        """
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update an existing record

        Args:
            db: SQLAlchemy database session
            db_obj: Existing model instance to update
            obj_in: Either a Pydantic model or dict with fields to update

        Returns:
            Updated model instance

        Example:
            ```python
            # Update with Pydantic model
            update_data = UserUpdate(is_active=False)
            user = user_crud.update(db, db_obj=existing_user, obj_in=update_data)

            # Update with dict
            user = user_crud.update(db, db_obj=existing_user, 
                                   obj_in={"is_active": False})
            ```

        Note:
            When using a Pydantic model, only set fields will be updated (exclude_unset=True).
            When using a dict, all provided keys will be updated.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[ModelType]:
        """
        Remove a record by ID

        Args:
            db: SQLAlchemy database session
            id: Primary key ID of the record to remove

        Returns:
            The removed model instance, or None if not found

        Example:
            ```python
            removed_user = user_crud.remove(db, id=1)
            ```

        Note:
            This performs a hard delete. For soft deletes, override this method
            in the specific CRUD class and set an is_active flag instead.
        """
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def count(self, db: Session, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count records with optional filters

        Args:
            db: SQLAlchemy database session
            filters: Optional dictionary of field-value pairs for filtering

        Returns:
            Integer count of matching records

        Example:
            ```python
            # Count all users
            total_users = user_crud.count(db)

            # Count active users
            active_count = user_crud.count(db, filters={"is_active": True})
            ```
        """
        query = db.query(func.count(self.model.id))

        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)

        return query.scalar()

    def exists(self, db: Session, id: Any) -> bool:
        """
        Check if record exists by ID

        Args:
            db: SQLAlchemy database session
            id: Primary key ID to check

        Returns:
            Boolean indicating if the record exists

        Example:
            ```python
            if user_crud.exists(db, id=1):
                # User exists
                pass
            ```
        """
        return db.query(self.model).filter(self.model.id == id).first() is not None

    def get_by_field(self, db: Session, field: str, value: Any) -> Optional[ModelType]:
        """
        Get a record by a specific field value

        Args:
            db: SQLAlchemy database session
            field: Name of the model field to filter on
            value: Value to match against the field

        Returns:
            Model instance if found, None otherwise

        Example:
            ```python
            user = user_crud.get_by_field(db, field="email", value="user@example.com")
            ```

        Note:
            This method only works if the field exists on the model.
            It performs an exact match (equality) comparison.
        """
        if hasattr(self.model, field):
            return db.query(self.model).filter(getattr(self.model, field) == value).first()
        return None

    def get_multi_by_field(
        self,
        db: Session,
        field: str,
        value: Any,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """
        Get multiple records by a specific field value with pagination

        Args:
            db: SQLAlchemy database session
            field: Name of the model field to filter on
            value: Value to match against the field
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return

        Returns:
            List of model instances matching the criteria

        Example:
            ```python
            # Get all books by a specific author
            books = book_crud.get_multi_by_field(
                db, field="author", value="Jane Austen", limit=20
            )
            ```

        Note:
            This method only works if the field exists on the model.
            It performs an exact match (equality) comparison.
        """
        if hasattr(self.model, field):
            return (
                db.query(self.model)
                .filter(getattr(self.model, field) == value)
                .offset(skip)
                .limit(limit)
                .all()
            )
        return []
