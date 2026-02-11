"""Security utilities."""
import re
from typing import Set


class SQLSecurityValidator:
    """Validates SQL queries for security risks."""

    # Dangerous patterns to block
    DANGEROUS_PATTERNS = [
        (r"\bdrop\s+database\b", "DROP DATABASE is not allowed"),
        (r"\btruncate\b", "TRUNCATE is not allowed"),
        (r";.*?(?:select|insert|update|delete|drop|alter|truncate)", "Multiple statements not allowed"),
    ]

    # Query type patterns
    QUERY_PATTERNS = {
        "SELECT": r"^\s*select\b",
        "INSERT": r"^\s*insert\b",
        "UPDATE": r"^\s*update\b",
        "DELETE": r"^\s*delete\b",
        "ALTER": r"^\s*alter\b",
    }

    @staticmethod
    def validate_query(query: str) -> tuple[bool, Optional[str]]:
        """
        Validate SQL query for dangerous patterns.

        Args:
            query: SQL query string

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Remove comments
        query_clean = re.sub(r"--.*?$", "", query, flags=re.MULTILINE)
        query_clean = re.sub(r"/\*.*?\*/", "", query_clean, flags=re.DOTALL)

        # Check for dangerous patterns (case-insensitive)
        for pattern, message in SQLSecurityValidator.DANGEROUS_PATTERNS:
            if re.search(pattern, query_clean, re.IGNORECASE):
                return False, message

        return True, None

    @staticmethod
    def require_where_for_delete(query: str) -> tuple[bool, Optional[str]]:
        """
        Require WHERE clause for DELETE statements.

        Args:
            query: SQL query string

        Returns:
            Tuple of (is_valid, error_message)
        """
        query_clean = re.sub(r"--.*?$", "", query, flags=re.MULTILINE)
        query_clean = re.sub(r"/\*.*?\*/", "", query_clean, flags=re.DOTALL)

        if re.search(r"^\s*delete\b", query_clean, re.IGNORECASE):
            if not re.search(r"\bwhere\b", query_clean, re.IGNORECASE):
                return False, "DELETE statements must include a WHERE clause"

        return True, None

    @staticmethod
    def inject_limit_to_select(query: str, limit: int = 100) -> str:
        """
        Inject LIMIT clause to SELECT if not present.

        Args:
            query: SQL query string
            limit: Limit value to inject

        Returns:
            Modified query with LIMIT clause
        """
        query_clean = re.sub(r"--.*?$", "", query, flags=re.MULTILINE)
        query_clean = re.sub(r"/\*.*?\*/", "", query_clean, flags=re.DOTALL)

        if re.search(r"^\s*select\b", query_clean, re.IGNORECASE):
            # Check if LIMIT already exists
            if not re.search(r"\blimit\b", query_clean, re.IGNORECASE):
                # Check for UNION, INTERSECT, EXCEPT
                if re.search(r"\b(union|intersect|except)\b", query_clean, re.IGNORECASE):
                    query = f"({query}) LIMIT {limit}"
                else:
                    query = f"{query.rstrip(';')} LIMIT {limit}"

        return query

    @staticmethod
    def get_query_type(query: str) -> Optional[str]:
        """
        Determine query type.

        Args:
            query: SQL query string

        Returns:
            Query type (SELECT, INSERT, UPDATE, DELETE, ALTER) or None
        """
        query_clean = re.sub(r"--.*?$", "", query, flags=re.MULTILINE)
        query_clean = re.sub(r"/\*.*?\*/", "", query_clean, flags=re.DOTALL)

        for query_type, pattern in SQLSecurityValidator.QUERY_PATTERNS.items():
            if re.search(pattern, query_clean, re.IGNORECASE):
                return query_type

        return None


def sanitize_connection_string(connection_string: str) -> str:
    """
    Remove sensitive information from connection string for logging.

    Args:
        connection_string: Database connection string

    Returns:
        Sanitized connection string
    """
    return re.sub(r"password=[^;]*", "password=***", connection_string, flags=re.IGNORECASE)
