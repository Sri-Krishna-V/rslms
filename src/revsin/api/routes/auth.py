"""
Authentication routes for the Library Management System

This module contains all API routes related to authentication, including:
- User registration
- User login
- OAuth2 token generation
- Current user information retrieval
- Token refresh

All authentication is JWT-based, with tokens that expire based on the configured
expiration time. The authentication flow follows OAuth2 standards.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Dict, Any

from ...database import get_db
from ...crud.user import user_crud
from ...schemas.user import UserCreate, UserResponse, Token, UserLogin
from ...auth.jwt_handler import create_access_token, authenticate_user
from ...auth.dependencies import get_current_active_user
from ...models.user import User
from ...config import settings

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_in: UserCreate = Body(
        ...,
        example={
            "email": "user@example.com",
            "username": "newuser",
            "first_name": "John",
            "last_name": "Doe",
            "password": "strongpassword123",
            "phone": "+1234567890",
            "address": "123 Main St, City",
            "role": "member"
        }
    ),
    db: Session = Depends(get_db)
):
    """
    Register a new user in the system

    This endpoint allows new users to register with the library system.
    It validates that the email and username are unique before creating the account.
    By default, new users are assigned the "member" role unless specified otherwise.

    The password is automatically hashed before storage in the database.

    Parameters:
    - **user_in**: User registration data containing all required fields

    Returns:
    - The created user information (without the password)

    Raises:
    - 400 Bad Request: If email is already registered
    - 400 Bad Request: If username is already taken
    """
    # Check if user already exists
    if user_crud.get_by_email(db, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    if user_crud.get_by_username(db, username=user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Create user
    user = user_crud.create(db, obj_in=user_in)
    return user


@router.post("/login", response_model=Token)
def login(
    user_credentials: UserLogin = Body(
        ...,
        example={
            "email": "user@example.com",
            "password": "strongpassword123"
        }
    ),
    db: Session = Depends(get_db)
):
    """
    User login endpoint

    This endpoint authenticates a user using email and password,
    and returns a JWT token that can be used for authenticated requests.

    The token will expire after the configured time (default: 30 minutes).

    Parameters:
    - **user_credentials**: User login credentials (email and password)

    Returns:
    - Access token and token type for authentication

    Raises:
    - 401 Unauthorized: If credentials are invalid

    Example response:
    ```json
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer"
    }
    ```

    Usage:
    After obtaining the token, include it in the Authorization header of subsequent requests:
    `Authorization: Bearer {token}`
    """
    user = authenticate_user(db, user_credentials.email,
                             user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login

    This endpoint follows the OAuth2 password flow standard for obtaining tokens.
    It's designed to be compatible with standard OAuth2 clients and tools.

    The username field should contain the user's email address.

    Parameters:
    - **form_data**: OAuth2 form with username (email) and password fields

    Returns:
    - Access token and token type for authentication

    Raises:
    - 401 Unauthorized: If credentials are invalid

    Note:
    This endpoint is primarily for OAuth2 compatibility. For regular API usage,
    the /login endpoint is recommended as it accepts JSON data.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current authenticated user information

    This endpoint returns information about the currently authenticated user
    based on the provided JWT token.

    Parameters:
    - **current_user**: Automatically extracted from the authentication token

    Returns:
    - Current user information including profile details and role

    Requires:
    - Valid authentication token in the Authorization header

    Example response:
    ```json
    {
        "id": 1,
        "email": "user@example.com",
        "username": "username",
        "first_name": "John",
        "last_name": "Doe",
        "phone": "+1234567890",
        "address": "123 Main St, City",
        "is_active": true,
        "role": "member",
        "full_name": "John Doe",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
    ```
    """
    return current_user


@router.post("/refresh", response_model=Token)
def refresh_token(current_user: User = Depends(get_current_active_user)):
    """
    Refresh access token

    This endpoint generates a new access token for the currently authenticated user.
    Use this endpoint when the current token is about to expire but the user session
    should remain active.

    Parameters:
    - **current_user**: Automatically extracted from the authentication token

    Returns:
    - New access token with reset expiration time

    Requires:
    - Valid (non-expired) authentication token in the Authorization header

    Security note:
    This is a simple token refresh mechanism. For production systems with higher
    security requirements, consider implementing refresh tokens separate from
    access tokens.
    """
    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": current_user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
