"""Transaction management for database operations."""
from typing import Any, Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.logger import logger


class TransactionManager:
    """Manage database transactions."""

    @staticmethod
    async def execute_with_transaction(
        session: AsyncSession,
        query: str,
    ) -> tuple[bool, Any, Optional[str]]:
        """
        Execute query within a transaction.

        Args:
            session: Database session
            query: SQL query to execute

        Returns:
            Tuple of (success, result, error_message)
        """
        try:
            # Start transaction (implicit in SQLAlchemy)
            result = await session.execute(text(query))

            # Check if query has results
            try:
                rows = result.fetchall()
                await session.commit()
                logger.info("Transaction committed successfully")
                return True, rows, None
            except Exception:
                # Write operation (INSERT, UPDATE, DELETE)
                rows_affected = result.rowcount
                await session.commit()
                logger.info(f"Transaction committed: {rows_affected} rows affected")
                return True, rows_affected, None

        except Exception as e:
            await session.rollback()
            error_msg = str(e)
            logger.error(f"Transaction failed and rolled back: {error_msg}")
            return False, None, error_msg

    @staticmethod
    async def execute_read_only(
        session: AsyncSession,
        query: str,
    ) -> tuple[bool, Any, Optional[str]]:
        """
        Execute read-only query (SELECT).

        Args:
            session: Database session
            query: SQL query to execute

        Returns:
            Tuple of (success, result, error_message)
        """
        try:
            result = await session.execute(text(query))
            rows = result.fetchall()
            logger.info(f"Read query executed successfully: {len(rows)} rows returned")
            return True, rows, None
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Read query failed: {error_msg}")
            return False, None, error_msg

    @staticmethod
    async def execute_preview_query(
        session: AsyncSession,
        query: str,
    ) -> tuple[bool, int, Optional[str]]:
        """
        Execute preview query (converted UPDATE/DELETE to SELECT).

        Args:
            session: Database session
            query: SQL query to execute

        Returns:
            Tuple of (success, affected_rows, error_message)
        """
        try:
            result = await session.execute(text(query))
            rows = result.fetchall()
            affected_rows = len(rows)
            logger.info(f"Preview query executed: {affected_rows} rows affected")
            return True, affected_rows, None
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Preview query failed: {error_msg}")
            return False, 0, error_msg

    @staticmethod
    def convert_update_to_select(query: str) -> str:
        """
        Convert UPDATE query to SELECT to preview affected rows.

        Args:
            query: UPDATE query string

        Returns:
            Converted SELECT query
        """
        # Simple conversion: extract WHERE clause and table name
        import re

        # Try to extract table name and WHERE clause
        match = re.match(r"UPDATE\s+([^\s]+).*?WHERE\s+(.+?)(?:;)?$", query, re.IGNORECASE | re.DOTALL)

        if match:
            table_name = match.group(1).strip()
            where_clause = match.group(2).strip()
            return f"SELECT * FROM {table_name} WHERE {where_clause}"

        # Fallback: just return the original as SELECT
        query_modified = re.sub(r"^UPDATE\b", "SELECT *", query, flags=re.IGNORECASE)
        query_modified = re.sub(
            r"SET\s+.*?\s+WHERE", " WHERE", query_modified, flags=re.IGNORECASE | re.DOTALL
        )
        return query_modified

    @staticmethod
    def convert_delete_to_select(query: str) -> str:
        """
        Convert DELETE query to SELECT to preview affected rows.

        Args:
            query: DELETE query string

        Returns:
            Converted SELECT query
        """
        import re

        # Convert DELETE to SELECT
        query_modified = re.sub(r"^DELETE\s+FROM\b", "SELECT * FROM", query, flags=re.IGNORECASE)
        return query_modified
