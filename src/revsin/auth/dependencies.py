"""
Authentication dependencies for FastAPI endpoints

This module provides dependency functions for FastAPI endpoints that enforce
various authentication and authorization requirements. These dependencies can
be used to protect API endpoints based on:

1. Authentication status (valid JWT token)
2. Account status (active/inactive)
3. User role (admin, librarian, member)

These dependencies are designed to be used with FastAPI's dependency injection system
and build upon each other in a hierarchical manner.
"""

from fastapi import HTTPException, status, Depends
from typing import Callable, Any
from ..models.user import User, UserRole
from .jwt_handler import get_current_user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to get the current active user

    This dependency ensures that the user is not only authenticated
    but also has an active account status. It builds on the get_current_user
    dependency which handles JWT token validation.

    Args:
        current_user: Current authenticated user from the token
                     (automatically injected by FastAPI)

    Returns:
        The authenticated user if active

    Raises:
        HTTPException(400): If the user account is inactive

    Usage:
        ```python
        @app.get("/users/me")
        def read_own_profile(user: User = Depends(get_current_active_user)):
            return user
        ```
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def get_current_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Dependency to get the current admin user

    This dependency ensures that the user is authenticated, active,
    and has the admin role. It's used to protect endpoints that should
    only be accessible by administrators.

    Args:
        current_user: Current active user from get_current_active_user
                     (automatically injected by FastAPI)

    Returns:
        The authenticated user if they have admin role

    Raises:
        HTTPException(403): If the user doesn't have admin role

    Usage:
        ```python
        @app.delete("/users/{user_id}")
        def delete_user(
            user_id: int,
            admin: User = Depends(get_current_admin_user)
        ):
            # Only admins can reach this point
            return {"message": f"User {user_id} deleted by admin {admin.username}"}
        ```
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


def get_current_librarian_user(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Dependency to get the current librarian or admin user

    This dependency ensures that the user is authenticated, active,
    and has either the librarian or admin role. It's used to protect
    endpoints that should only be accessible by library staff.

    Args:
        current_user: Current active user from get_current_active_user
                     (automatically injected by FastAPI)

    Returns:
        The authenticated user if they have librarian or admin role

    Raises:
        HTTPException(403): If the user doesn't have librarian or admin role

    Usage:
        ```python
        @app.post("/books/")
        def add_book(
            book_data: BookCreate,
            staff: User = Depends(get_current_librarian_user)
        ):
            # Only librarians and admins can reach this point
            return {"message": f"Book added by {staff.username}"}
        ```
    """
    if current_user.role not in [UserRole.LIBRARIAN, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


def get_current_member_user(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Dependency to get the current member user (any active user)

    This dependency ensures that the user is authenticated and active.
    It accepts users with any role (member, librarian, admin) and is used
    for endpoints that should be accessible to all authenticated users.

    This is functionally equivalent to get_current_active_user but has a
    more descriptive name for API endpoints that are specifically meant
    for library members.

    Args:
        current_user: Current active user from get_current_active_user
                     (automatically injected by FastAPI)

    Returns:
        The authenticated user (any role)

    Usage:
        ```python
        @app.get("/books/borrow/{book_id}")
        def borrow_book(
            book_id: int,
            member: User = Depends(get_current_member_user)
        ):
            # Any authenticated user can borrow a book
            return {"message": f"Book {book_id} borrowed by {member.username}"}
        ```
    """
    return current_user


def get_owner_or_admin(resource_owner_id_field: str) -> Callable:
    """
    Factory function to create a dependency that checks if the current user
    is either the owner of a resource or an admin

    This creates a dependency that can be used to protect endpoints where
    users should only be able to access their own resources, but admins
    can access any resource.

    Args:
        resource_owner_id_field: The name of the path parameter that contains
                                the resource owner's ID

    Returns:
        A dependency function that checks ownership or admin status

    Usage:
        ```python
        @app.put("/users/{user_id}")
        def update_user(
            user_id: int,
            user_data: UserUpdate,
            current_user: User = Depends(get_owner_or_admin("user_id"))
        ):
            # Only the user themselves or an admin can update the user
            return {"message": f"User {user_id} updated"}
        ```
    """
    def check_owner_or_admin(
        current_user: User = Depends(get_current_active_user),
        **path_params
    ) -> User:
        resource_owner_id = path_params.get(resource_owner_id_field)

        # Allow if user is admin or the owner of the resource
        if (current_user.role == UserRole.ADMIN or
                current_user.id == int(resource_owner_id)):
            return current_user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    return check_owner_or_admin
