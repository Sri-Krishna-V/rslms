"""
JWT authentication handler for the Library Management System

This module implements JWT (JSON Web Token) based authentication for the API.
It provides functions for:
- Creating JWT tokens with configurable expiration
- Verifying and decoding JWT tokens
- Extracting the current user from a request
- Authenticating user credentials

The authentication flow follows OAuth2 standards with Bearer tokens.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..crud.user import user_crud
from ..schemas.user import TokenData
from ..models.user import User

# Security scheme for Swagger UI
security = HTTPBearer(
    description="JWT Bearer token authentication",
    scheme_name="Bearer"
)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token

    This function generates a new JWT token containing the provided data,
    with an expiration time either specified or derived from settings.

    Args:
        data: Dictionary containing data to encode in the token
              Should include a 'sub' key with the user's identifier (email)
        expires_delta: Optional custom expiration time
                      If not provided, uses the configured default

    Returns:
        Encoded JWT token string

    Example:
        ```python
        # Create token with default expiration
        token = create_access_token(data={"sub": user.email})

        # Create token with custom expiration
        token = create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(hours=1)
        )
        ```

    Security note:
        The token is signed using the application's secret key.
        Ensure this key is kept secure and has sufficient entropy.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str, credentials_exception: HTTPException) -> TokenData:
    """
    Verify JWT token and extract user data

    This function decodes and validates a JWT token, extracting the user
    email from the 'sub' claim.

    Args:
        token: JWT token string to verify
        credentials_exception: Exception to raise if verification fails

    Returns:
        TokenData object containing the user's email

    Raises:
        HTTPException: If the token is invalid, expired, or missing required claims

    Security checks performed:
    - Token signature validation using the secret key
    - Token expiration check (handled by the JWT library)
    - Presence of 'sub' claim containing user email
    """
    try:
        # Decode the JWT token
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        # Extract email from the 'sub' claim
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        # Create token data with email
        token_data = TokenData(email=email)

    except JWTError:
        # Any JWT decoding error results in authentication failure
        raise credentials_exception

    return token_data


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from request

    This function extracts and validates the JWT token from the request,
    then retrieves the corresponding user from the database.

    Args:
        credentials: Authorization credentials from the request header
                    Automatically extracted by FastAPI from the Authorization header
        db: Database session

    Returns:
        User object for the authenticated user

    Raises:
        HTTPException(401): If authentication fails for any reason:
                           - Missing token
                           - Invalid token
                           - Expired token
                           - User not found

    Usage:
        ```python
        @app.get("/protected")
        def protected_route(current_user: User = Depends(get_current_user)):
            return {"message": f"Hello, {current_user.username}!"}
        ```
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Extract token from credentials
    token = credentials.credentials

    # Verify token and get token data
    token_data = verify_token(token, credentials_exception)

    # Get user from database using email
    user = user_crud.get_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception

    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticate user credentials

    This function verifies user credentials against the database.
    It checks both the email/password combination and if the user is active.

    Args:
        db: Database session
        email: User email address
        password: User password (plain text)

    Returns:
        User object if authentication is successful, None otherwise

    Security notes:
    - Password verification is performed using secure hashing in the user_crud
    - No details about the failure reason are returned to avoid information leakage
    - Inactive users cannot authenticate even with correct credentials

    Example:
        ```python
        user = authenticate_user(db, "user@example.com", "password123")
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        ```
    """
    # Verify email/password combination
    user = user_crud.authenticate(db, email=email, password=password)
    if not user:
        return None

    # Check if user is active
    if not user_crud.is_active(user):
        return None

    return user
