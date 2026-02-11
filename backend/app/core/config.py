"""Configuration management for the application."""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration."""

    # API Configuration
    api_title: str = "Text to SQL API"
    api_version: str = "1.0.0"
    api_description: str = "AI-powered SQL generator using Gemini"
    debug: bool = False

    # Database Configuration
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "postgres"
    db_user: str = "postgres"
    db_password: str = "password"
    db_pool_size: int = 20
    db_max_overflow: int = 10
    db_pool_recycle: int = 3600
    db_echo: bool = False

    # Gemini Configuration
    gemini_api_key: str
    gemini_model: str = "gemini-2.0-flash"
    gemini_temperature: float = 0.3
    gemini_max_tokens: int = 2048

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Query Configuration
    max_query_length: int = 10000
    default_result_limit: int = 100
    max_result_limit: int = 1000

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
