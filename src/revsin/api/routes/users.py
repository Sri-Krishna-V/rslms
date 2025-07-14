"""
Users routes for the Library Management System

This module contains all API routes related to user management, including:
- Listing all users (admin only)
- Retrieving user details
- Updating user information
- Deleting users
- Searching for users

All routes in this module require authentication, and some operations
are restricted to users with specific roles (admin, librarian).
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional

from ...database import get_db
from ...crud.user import user_crud
from ...schemas.user import UserResponse, UserUpdate
from ...auth.dependencies import get_current_admin_user, get_current_active_user
from ...models.user import User, UserRole

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = Query(0, description="Number of users to skip for pagination"),
    limit: int = Query(100, description="Maximum number of users to return"),
    role: Optional[UserRole] = Query(None, description="Filter users by role"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Get all users (admin only)

    This endpoint returns a list of all users in the system.
    Results can be paginated using skip/limit parameters and filtered by role.

    Parameters:
    - **skip**: Number of users to skip (for pagination)
    - **limit**: Maximum number of users to return
    - **role**: Optional filter by user role (admin, librarian, member)

    Returns:
    - List of users with their details

    Requires:
    - Authentication with admin role

    Example response:
    ```json
    [
        {
            "id": 1,
            "email": "admin@example.com",
            "username": "admin",
            "first_name": "Admin",
            "last_name": "User",
            "is_active": true,
            "role": "admin",
            "full_name": "Admin User",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        },
        {
            "id": 2,
            "email": "user@example.com",
            "username": "user",
            "first_name": "Regular",
            "last_name": "User",
            "is_active": true,
            "role": "member",
            "full_name": "Regular User",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
    ]
    ```
    """
    if role:
        users = user_crud.get_by_role(db, role=role, skip=skip, limit=limit)
    else:
        users = user_crud.get_multi(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int = Path(...,
                        description="The ID of the user to retrieve", gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get user by ID

    This endpoint retrieves detailed information about a specific user.
    Regular users can only access their own profile, while admins can access any user.

    Parameters:
    - **user_id**: The unique identifier of the user

    Returns:
    - User details if found

    Raises:
    - 404 Not Found: If user doesn't exist
    - 403 Forbidden: If a non-admin user tries to access another user's profile

    Security:
    - Regular users can only view their own profile
    - Admins can view any user's profile
    """
    # Check if user is trying to access their own profile or is an admin
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's information"
        )

    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int = Path(..., description="The ID of the user to update", gt=0),
    user_in: UserUpdate = ...,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update user information

    This endpoint allows updating user information. Regular users can only update
    their own profile, while admins can update any user.

    Role changes can only be performed by admins.

    Parameters:
    - **user_id**: The unique identifier of the user to update
    - **user_in**: Updated user data

    Returns:
    - Updated user information

    Raises:
    - 404 Not Found: If user doesn't exist
    - 403 Forbidden: If a non-admin user tries to update another user's profile
                     or if a non-admin tries to change roles

    Notes:
    - Password updates will automatically hash the new password
    - Only fields that are provided will be updated
    """
    # Check if user exists
    db_user = user_crud.get(db, id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check permissions
    is_admin = current_user.role == UserRole.ADMIN
    is_self = current_user.id == user_id

    if not (is_admin or is_self):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )

    # Only admins can change roles
    if user_in.role and user_in.role != db_user.role and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to change user role"
        )

    # Update user
    updated_user = user_crud.update(db, db_obj=db_user, obj_in=user_in)
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int = Path(..., description="The ID of the user to delete", gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Delete user (admin only)

    This endpoint allows admins to delete a user from the system.

    Parameters:
    - **user_id**: The unique identifier of the user to delete

    Returns:
    - 204 No Content on successful deletion

    Raises:
    - 404 Not Found: If user doesn't exist

    Notes:
    - This operation is irreversible
    - All associated data (loans, etc.) will be affected according to database constraints
    """
    # Check if user exists
    db_user = user_crud.get(db, id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Delete user
    user_crud.remove(db, id=user_id)
    return None


@router.get("/search/", response_model=List[UserResponse])
def search_users(
    query: str = Query(...,
                       description="Search query (name, email, username)"),
    skip: int = Query(0, description="Number of users to skip for pagination"),
    limit: int = Query(100, description="Maximum number of users to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Search users (admin only)

    This endpoint allows searching for users by name, email, or username.

    Parameters:
    - **query**: Search term to match against name, email, or username
    - **skip**: Number of users to skip (for pagination)
    - **limit**: Maximum number of users to return

    Returns:
    - List of users matching the search criteria

    Requires:
    - Authentication with admin role

    Example:
    ```
    GET /api/v1/users/search/?query=john
    ```

    Will return users with "john" in their name, email, or username.
    """
    users = user_crud.search(db, query=query, skip=skip, limit=limit)
    return users
