"""
Database connection configuration for NeonDB PostgreSQL
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config import settings
from ..models.base import Base
import logging

logger = logging.getLogger(__name__)

# Database engine configuration
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10,
    echo=settings.debug,
    connect_args={
        "sslmode": "require",
        "connect_timeout": 10,
        "application_name": "revsin_library_system"
    }
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def get_db():
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database with tables"""
    create_tables()
    logger.info("Database initialized successfully")
