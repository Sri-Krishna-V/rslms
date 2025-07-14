"""
Configuration settings for the Library Management System

This module defines all configuration settings for the application,
loaded from environment variables with sensible defaults.
"""

import os
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Dict, Any, Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database Configuration
    database_url: str = Field(
        default="postgresql://username:password@hostname:5432/database_name",
        description="PostgreSQL database URL for NeonDB"
    )

    database_url_async: str = Field(
        default="postgresql+asyncpg://username:password@hostname:5432/database_name",
        description="Async PostgreSQL database URL for NeonDB"
    )

    # Redis Configuration
    redis_url: str = Field(
        default="redis://default:password@hostname:port",
        description="Redis URL for Upstash"
    )

    # Security Configuration
    secret_key: str = Field(
        default="your-secret-key-here-change-this-in-production",
        description="Secret key for JWT token generation"
    )

    algorithm: str = Field(
        default="HS256",
        description="Algorithm for JWT token generation"
    )

    access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration time in minutes"
    )

    # Application Configuration
    environment: str = Field(
        default="development",
        description="Application environment"
    )

    debug: bool = Field(
        default=True,
        description="Debug mode"
    )

    # CORS Configuration
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="CORS allowed origins"
    )

    # Cache Configuration
    cache_expire_time: int = Field(
        default=300,
        description="Default cache expiration time in seconds"
    )

    # Logging Configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )

    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log message format"
    )

    # Server Configuration
    host: str = Field(
        default="0.0.0.0",
        description="Host to bind the server to"
    )

    port: int = Field(
        default=8000,
        description="Port to bind the server to"
    )

    workers: int = Field(
        default=4,
        description="Number of worker processes (recommended: 2 * CPU cores + 1)"
    )

    # Security Settings
    https_only: bool = Field(
        default=False,
        description="Enforce HTTPS only (for production)"
    )

    hsts_enabled: bool = Field(
        default=False,
        description="Enable HTTP Strict Transport Security"
    )

    @validator("debug", pre=True)
    def set_debug_based_on_environment(cls, v, values):
        """Set debug mode based on environment if not explicitly set"""
        if "environment" in values and values["environment"] == "production":
            return False
        return v

    @property
    def is_production(self) -> bool:
        """Check if the application is running in production mode"""
        return self.environment.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if the application is running in development mode"""
        return self.environment.lower() == "development"

    @property
    def is_testing(self) -> bool:
        """Check if the application is running in testing mode"""
        return self.environment.lower() == "testing"

    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration dictionary"""
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": self.log_format,
                },
            },
            "handlers": {
                "console": {
                    "level": self.log_level,
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
                "file": {
                    "level": self.log_level,
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": "logs/revsin.log",
                    "maxBytes": 10485760,  # 10 MB
                    "backupCount": 5,
                    "formatter": "default",
                } if self.is_production else {
                    "class": "logging.NullHandler",
                },
            },
            "loggers": {
                "revsin": {
                    "handlers": ["console", "file"] if self.is_production else ["console"],
                    "level": self.log_level,
                    "propagate": False,
                },
                "uvicorn": {
                    "handlers": ["console"],
                    "level": self.log_level,
                    "propagate": False,
                },
                "sqlalchemy": {
                    "handlers": ["console"],
                    "level": "WARNING",
                    "propagate": False,
                },
            },
            "root": {
                "handlers": ["console"],
                "level": self.log_level,
            },
        }

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()

# Ensure logs directory exists if in production
if settings.is_production and not os.path.exists("logs"):
    os.makedirs("logs")
