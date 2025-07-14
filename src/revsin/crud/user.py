"""
User CRUD operations for the Library Management System
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from passlib.context import CryptContext

from .base import CRUDBase
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..database.redis_client import cache, get_user_cache_key

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """CRUD operations for User model"""

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """Get user by email"""
        # Try cache first
        cache_key = f"user:email:{email}"
        cached_user = cache.get(cache_key)
        if cached_user:
            return User(**cached_user)

        # Query database
        user = db.query(User).filter(User.email == email).first()
        if user:
            # Cache the result
            user_dict = {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "hashed_password": user.hashed_password,
                "is_active": user.is_active,
                "role": user.role.value,
                "phone": user.phone,
                "address": user.address,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat()
            }
            cache.set(cache_key, user_dict)
            cache.set(get_user_cache_key(user.id), user_dict)

        return user

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """Get user by username"""
        # Try cache first
        cache_key = f"user:username:{username}"
        cached_user = cache.get(cache_key)
        if cached_user:
            return User(**cached_user)

        # Query database
        user = db.query(User).filter(User.username == username).first()
        if user:
            # Cache the result
            user_dict = {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "hashed_password": user.hashed_password,
                "is_active": user.is_active,
                "role": user.role.value,
                "phone": user.phone,
                "address": user.address,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat()
            }
            cache.set(cache_key, user_dict)
            cache.set(get_user_cache_key(user.id), user_dict)

        return user

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """Create a new user with hashed password"""
        obj_in_data = obj_in.dict()
        password = obj_in_data.pop("password")
        hashed_password = self.get_password_hash(password)

        db_obj = User(**obj_in_data, hashed_password=hashed_password)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # Cache the new user
        user_dict = {
            "id": db_obj.id,
            "email": db_obj.email,
            "username": db_obj.username,
            "first_name": db_obj.first_name,
            "last_name": db_obj.last_name,
            "hashed_password": db_obj.hashed_password,
            "is_active": db_obj.is_active,
            "role": db_obj.role.value,
            "phone": db_obj.phone,
            "address": db_obj.address,
            "created_at": db_obj.created_at.isoformat(),
            "updated_at": db_obj.updated_at.isoformat()
        }
        cache.set(get_user_cache_key(db_obj.id), user_dict)
        cache.set(f"user:email:{db_obj.email}", user_dict)
        cache.set(f"user:username:{db_obj.username}", user_dict)

        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        """Update user with optional password change"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if "password" in update_data:
            password = update_data.pop("password")
            update_data["hashed_password"] = self.get_password_hash(password)

        updated_user = super().update(db, db_obj=db_obj, obj_in=update_data)

        # Invalidate cache
        cache.delete(get_user_cache_key(updated_user.id))
        cache.delete(f"user:email:{updated_user.email}")
        cache.delete(f"user:username:{updated_user.username}")

        return updated_user

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """Authenticate user by email and password"""
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        """Check if user is active"""
        return user.is_active

    def search_users(self, db: Session, *, query: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Search users by name, email, or username"""
        return (
            db.query(User)
            .filter(
                or_(
                    User.first_name.ilike(f"%{query}%"),
                    User.last_name.ilike(f"%{query}%"),
                    User.email.ilike(f"%{query}%"),
                    User.username.ilike(f"%{query}%")
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_users(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[User]:
        """Get active users"""
        return (
            db.query(User)
            .filter(User.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash password"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password"""
        return pwd_context.verify(plain_password, hashed_password)


user_crud = CRUDUser(User)
