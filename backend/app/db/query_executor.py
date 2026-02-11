"""Query execution with safety checks."""
from typing import Any, Dict, List, Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.query_validator import QueryValidator
from app.db.transaction_manager import TransactionManager
from app.utils.logger import logger


class QueryExecutor:
    """Execute SQL queries safely."""

    @staticmethod
    async def execute_query(
        session: AsyncSession,
        query: str,
    ) -> Dict[str, Any]:
        """
        Execute SQL query with validation.

        Args:
            session: Database session
            query: SQL query to execute

        Returns:
            Dictionary with execution result
        """
        # Validate query
        is_valid, error, query_type = QueryValidator.validate_generated_query(query)
        if not is_valid:
            return {
                "success": False,
                "error": error,
                "query_type": None,
                "affected_rows": 0,
                "data": None,
            }

        # Execute based on query type
        if query_type == "SELECT":
            success, result, error = await TransactionManager.execute_read_only(session, query)

            if success:
                rows = [dict(row._mapping) for row in result]
                return {
                    "success": True,
                    "query_type": query_type,
                    "data": rows,
                    "rows_returned": len(rows),
                    "error": None,
                }
            else:
                return {
                    "success": False,
                    "query_type": query_type,
                    "error": error,
                    "data": None,
                    "rows_returned": 0,
                }

        else:
            # Write operation
            success, rows_affected, error = await TransactionManager.execute_with_transaction(session, query)

            if success:
                return {
                    "success": True,
                    "query_type": query_type,
                    "affected_rows": rows_affected if isinstance(rows_affected, int) else 0,
                    "error": None,
                }
            else:
                return {
                    "success": False,
                    "query_type": query_type,
                    "error": error,
                    "affected_rows": 0,
                }

    @staticmethod
    async def preview_query(
        session: AsyncSession,
        query: str,
    ) -> Dict[str, Any]:
        """
        Preview query to show affected rows without executing write operation.

        Args:
            session: Database session
            query: SQL query to preview

        Returns:
            Dictionary with preview result
        """
        # Validate query
        is_valid, error = QueryValidator.validate_preview_query(query)
        if not is_valid:
            return {
                "success": False,
                "error": error,
                "preview_rows": [],
                "affected_rows": 0,
            }

        query_type = QueryValidator.validate_generated_query(query)[2]

        # Convert UPDATE/DELETE to SELECT for preview
        if query_type == "UPDATE":
            preview_query = TransactionManager.convert_update_to_select(query)
        elif query_type == "DELETE":
            preview_query = TransactionManager.convert_delete_to_select(query)
        else:
            preview_query = query

        # Execute preview
        success, affected_rows, error = await TransactionManager.execute_preview_query(session, preview_query)

        if success:
            # For preview, try to get actual data
            try:
                result = await session.execute(text(preview_query))
                rows = result.fetchall()
                preview_data = [dict(row._mapping) for row in rows[:100]]  # Limit preview

                return {
                    "success": True,
                    "query_type": query_type,
                    "preview_rows": preview_data,
                    "affected_rows": affected_rows,
                    "error": None,
                }
            except Exception as e:
                return {
                    "success": False,
                    "query_type": query_type,
                    "error": str(e),
                    "preview_rows": [],
                    "affected_rows": 0,
                }
        else:
            return {
                "success": False,
                "query_type": query_type,
                "error": error,
                "preview_rows": [],
                "affected_rows": 0,
            }
