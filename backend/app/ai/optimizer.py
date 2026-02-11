"""SQL query optimization suggestions."""
from typing import Any, Dict
from app.ai.sql_generator import sql_generator
from app.utils.logger import logger


class SQLOptimizer:
    """Optimize SQL queries."""

    @staticmethod
    async def get_optimization_suggestions(
        sql_query: str,
        schema_metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Get optimization suggestions for SQL query.

        Args:
            sql_query: SQL query to optimize
            schema_metadata: Database schema metadata

        Returns:
            Dictionary with optimization suggestions
        """
        try:
            result = await sql_generator.optimize_sql(sql_query, schema_metadata)
            return result
        except Exception as e:
            logger.error(f"Failed to optimize query: {str(e)}")
            return {
                "success": False,
                "error": str(e),
            }

    @staticmethod
    def check_common_issues(sql_query: str) -> Dict[str, Any]:
        """
        Check for common SQL issues.

        Args:
            sql_query: SQL query string

        Returns:
            Dictionary with identified issues
        """
        issues = []

        # Check for SELECT *
        if "SELECT *" in sql_query.upper():
            issues.append({
                "severity": "medium",
                "message": "Using SELECT * can be inefficient. Specify needed columns.",
            })

        # Check for missing indexes flags
        import re

        # Check for LIKE without index-friendly pattern
        if re.search(r"LIKE\s+'%", sql_query, re.IGNORECASE):
            issues.append({
                "severity": "medium",
                "message": "LIKE with leading % wildcard cannot use indexes efficiently.",
            })

        # Check for implicit type conversion
        if re.search(r"WHERE\s+\w+\s*=\s*'", sql_query, re.IGNORECASE):
            issues.append({
                "severity": "low",
                "message": "Check for implicit type conversion in WHERE clause.",
            })

        # Check for multiple JOINs without aggregation
        join_count = len(re.findall(r"JOIN", sql_query, re.IGNORECASE))
        if join_count > 3:
            issues.append({
                "severity": "low",
                "message": f"Query has {join_count} JOINs. Consider breaking into multiple queries.",
            })

        # Check for missing LIMIT on SELECT
        if re.search(r"^\s*SELECT\b", sql_query, re.IGNORECASE) and not re.search(
            r"LIMIT\b", sql_query, re.IGNORECASE
        ):
            issues.append({
                "severity": "high",
                "message": "SELECT without LIMIT could return many rows. Add LIMIT clause.",
            })

        return {
            "success": True,
            "issues": issues,
            "issue_count": len(issues),
        }
