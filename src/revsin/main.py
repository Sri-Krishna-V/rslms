"""
Main FastAPI application for the Library Management System
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from .config import settings
from .database.connection import init_db
from .api.routes import auth, users, books, loans

# Configure logging
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler
    """
    # Startup
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

    yield

    # Shutdown
    logger.info("Application shutting down")


# Create FastAPI application
app = FastAPI(
    title="Library Management System",
    description="""
    A comprehensive library management system with FastAPI, PostgreSQL, and Redis.
    
    ## Features
    
    * **User Management**: Registration, authentication, and role-based access control
    * **Book Management**: Add, update, search, and manage book inventory
    * **Loan Management**: Book borrowing, returning, renewals, and fine management
    * **Caching**: Redis-based caching for improved performance
    
    ## Authentication
    
    Most endpoints require authentication using a JWT token.
    1. Register a new user or login with existing credentials
    2. Use the returned token in the Authorization header: `Bearer {token}`
    
    ## Roles
    
    * **Admin**: Full access to all resources
    * **Librarian**: Can manage books and loans
    * **Member**: Can borrow books and view their loans
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs" if settings.environment == "production" else "/docs",
    redoc_url="/api/redoc" if settings.environment == "production" else "/redoc",
    openapi_url="/api/openapi.json" if settings.environment == "production" else "/openapi.json",
    contact={
        "name": "RevSin Support",
        "url": "https://github.com/yourusername/revsin/issues",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(books.router, prefix="/api/v1/books", tags=["books"])
app.include_router(loans.router, prefix="/api/v1/loans", tags=["loans"])


@app.get("/", tags=["health"])
async def root():
    """
    Root endpoint
    
    Returns basic information about the API.
    """
    return {
        "message": "Welcome to the Library Management System",
        "version": "1.0.0",
        "status": "active",
        "docs_url": "/api/docs" if settings.environment == "production" else "/docs"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint
    
    Returns the current health status of the application.
    Used by monitoring systems to check if the application is running correctly.
    """
    return {
        "status": "healthy",
        "environment": settings.environment,
        "debug": settings.debug
    }


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """
    Custom 404 handler
    """
    logger.warning(f"Resource not found: {request.url}")
    return JSONResponse(
        status_code=404,
        content={"message": "Resource not found"}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """
    Custom 500 handler
    """
    logger.error(f"Internal server error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.revsin.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
