"""Database connection management."""
from typing import AsyncIterator, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

from app.core.config import get_settings
from app.utils.logger import logger


class ConnectionManager:
    """Manage database connections."""

    def __init__(self):
        """Initialize connection manager."""
        self.settings = get_settings()
        self.engine: Optional[AsyncEngine] = None
        self.async_session_maker: Optional[sessionmaker] = None

    async def initialize(self) -> None:
        """Initialize async database engine and session factory."""
        try:
            # Build async connection URL
            connection_url = (
                f"postgresql+asyncpg://{self.settings.db_user}:"
                f"{self.settings.db_password}@{self.settings.db_host}:"
                f"{self.settings.db_port}/{self.settings.db_name}"
            )

            self.engine = create_async_engine(
                connection_url,
                echo=self.settings.db_echo,
                pool_size=self.settings.db_pool_size,
                max_overflow=self.settings.db_max_overflow,
                pool_recycle=self.settings.db_pool_recycle,
                pool_pre_ping=True,
            )

            self.async_session_maker = sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=False,
                autocommit=False,
            )

            logger.info("Database connection pool initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database connection: {str(e)}")
            raise

    async def close(self) -> None:
        """Close database engine."""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database connection pool closed")

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        """
        Get async database session.

        Yields:
            AsyncSession instance
        """
        if not self.async_session_maker:
            raise RuntimeError("Database not initialized. Call initialize() first.")

        session = self.async_session_maker()
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Session error: {str(e)}")
            raise
        finally:
            await session.close()

    async def test_connection(self) -> bool:
        """
        Test database connection.

        Returns:
            True if connection successful
        """
        try:
            async with self.get_session() as session:
                await session.execute(text("SELECT 1"))
            logger.info("Database connection test successful")
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {str(e)}")
            return False


# Global connection manager instance
connection_manager = ConnectionManager()
