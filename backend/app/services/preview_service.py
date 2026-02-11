"""Query preview service."""
from typing import Any, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.query_executor import QueryExecutor
from app.utils.logger import logger


class PreviewService:
    """Service for previewing query results."""

    @staticmethod
    async def preview_query(
        session: AsyncSession,
        query: str,
    ) -> Dict[str, Any]:
        """
        Preview query results.

        Args:
            session: Database session
            query: SQL query to preview

        Returns:
            Dictionary with preview results
        """
        try:
            result = await QueryExecutor.preview_query(session, query)
            return result
        except Exception as e:
            logger.error(f"Failed to preview query: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "preview_rows": [],
                "affected_rows": 0,
            }

    @staticmethod
    async def preview_with_limit(
        session: AsyncSession,
        query: str,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """
        Preview query with row limit.

        Args:
            session: Database session
            query: SQL query to preview
            limit: Maximum rows to return

        Returns:
            Dictionary with preview results
        """
        try:
            # Add LIMIT clause if not present
            import re

            if not re.search(r"LIMIT\b", query, re.IGNORECASE):
                # Handle UNION/INTERSECT/EXCEPT
                if re.search(r"\b(UNION|INTERSECT|EXCEPT)\b", query, re.IGNORECASE):
                    query = f"({query}) LIMIT {limit}"
                else:
                    query = f"{query.rstrip(';')} LIMIT {limit}"

            result = await QueryExecutor.preview_query(session, query)
            return result
        except Exception as e:
            logger.error(f"Failed to preview query with limit: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "preview_rows": [],
                "affected_rows": 0,
            }

    @staticmethod
    def format_preview_result(
        rows: List[Dict[str, Any]],
        affected_rows: int,
        query_type: str,
    ) -> Dict[str, Any]:
        """
        Format preview result for API response.

        Args:
            rows: Preview row data
            affected_rows: Number of affected rows
            query_type: Type of query

        Returns:
            Formatted result dictionary
        """
        return {
            "query_type": query_type,
            "preview_rows": rows,
            "total_rows": affected_rows,
            "row_count_shown": len(rows),
            "message": f"Preview showing {len(rows)} of {affected_rows} rows that will be affected",
        }
