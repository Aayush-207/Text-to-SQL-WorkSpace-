"""SQL query validation."""
from typing import Optional, Tuple
from app.core.security import SQLSecurityValidator
from app.utils.logger import logger


class QueryValidator:
    """Validate SQL queries."""

    @staticmethod
    def validate_generated_query(query: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validate generated SQL query.

        Args:
            query: SQL query string

        Returns:
            Tuple of (is_valid, error_message, query_type)
        """
        # Check for dangerous patterns
        is_safe, error = SQLSecurityValidator.validate_query(query)
        if not is_safe:
            logger.warning(f"Unsafe query detected: {error}")
            return False, error, None

        # Check for DELETE without WHERE
        is_safe, error = SQLSecurityValidator.require_where_for_delete(query)
        if not is_safe:
            logger.warning(f"Unsafe DELETE detected: {error}")
            return False, error, None

        # Get query type
        query_type = SQLSecurityValidator.get_query_type(query)
        if not query_type:
            return False, "Could not determine query type", None

        # Inject LIMIT for SELECT
        if query_type == "SELECT":
            query = SQLSecurityValidator.inject_limit_to_select(query)

        logger.info(f"Query validated successfully: {query_type}")
        return True, None, query_type

    @staticmethod
    def validate_preview_query(query: str) -> Tuple[bool, Optional[str]]:
        """
        Validate query for preview (converts UPDATE/DELETE to SELECT).

        Args:
            query: SQL query string

        Returns:
            Tuple of (is_valid, error_message)
        """
        is_safe, error = SQLSecurityValidator.validate_query(query)
        if not is_safe:
            return False, error

        return True, None

    @staticmethod
    def is_write_query(query_type: Optional[str]) -> bool:
        """
        Check if query is a write operation.

        Args:
            query_type: Query type (SELECT, INSERT, UPDATE, DELETE, ALTER)

        Returns:
            True if query is a write operation
        """
        return query_type in ["INSERT", "UPDATE", "DELETE", "ALTER"]

    @staticmethod
    def is_read_query(query_type: Optional[str]) -> bool:
        """
        Check if query is a read operation.

        Args:
            query_type: Query type

        Returns:
            True if query is a read operation
        """
        return query_type == "SELECT"
