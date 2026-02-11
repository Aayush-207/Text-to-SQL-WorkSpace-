"""SQL query explanation and analysis."""
from typing import Any, Dict, Optional
from app.ai.sql_generator import sql_generator
from app.utils.logger import logger


class SQLExplainer:
    """Explain SQL queries."""

    @staticmethod
    async def explain_query(sql_query: str) -> Dict[str, Any]:
        """
        Explain SQL query using AI.

        Args:
            sql_query: SQL query to explain

        Returns:
            Dictionary with explanation
        """
        try:
            result = await sql_generator.explain_sql(sql_query)
            return result
        except Exception as e:
            logger.error(f"Failed to explain query: {str(e)}")
            return {
                "success": False,
                "error": str(e),
            }

    @staticmethod
    def extract_query_metadata(sql_query: str) -> Dict[str, Any]:
        """
        Extract metadata from SQL query (tables, columns, joins).

        Args:
            sql_query: SQL query string

        Returns:
            Dictionary with extracted metadata
        """
        import re

        metadata = {
            "tables": [],
            "columns": [],
            "joins": [],
            "where_conditions": [],
        }

        try:
            # Extract table names (simple regex, not perfect)
            from_pattern = r"(?:FROM|JOIN)\s+([a-zA-Z0-9_\.\"]+)"
            tables = re.findall(from_pattern, sql_query, re.IGNORECASE)
            metadata["tables"] = [t.strip('"') for t in tables]

            # Extract column names (simple extraction)
            select_pattern = r"SELECT\s+(.+?)\s+FROM"
            select_match = re.search(select_pattern, sql_query, re.IGNORECASE | re.DOTALL)
            if select_match:
                columns_str = select_match.group(1)
                # Split by comma but not inside functions
                columns = [c.strip() for c in columns_str.split(",")]
                metadata["columns"] = columns

            # Extract JOIN conditions
            join_pattern = r"(?:INNER\s+|LEFT\s+|RIGHT\s+|FULL\s+)?JOIN\s+([a-zA-Z0-9_\.\"]+)\s+(?:ON|USING)\s+(.+?)(?:WHERE|GROUP|ORDER|;|$)"
            joins = re.findall(join_pattern, sql_query, re.IGNORECASE | re.DOTALL)
            metadata["joins"] = [{"table": j[0].strip('"'), "condition": j[1].strip()} for j in joins]

            # Extract WHERE conditions
            where_pattern = r"WHERE\s+(.+?)(?:GROUP|ORDER|LIMIT|;|$)"
            where_match = re.search(where_pattern, sql_query, re.IGNORECASE | re.DOTALL)
            if where_match:
                conditions = where_match.group(1).strip()
                # Split by AND/OR
                conds = re.split(r"\s+(?:AND|OR)\s+", conditions, flags=re.IGNORECASE)
                metadata["where_conditions"] = conds

            return metadata

        except Exception as e:
            logger.error(f"Failed to extract query metadata: {str(e)}")
            return metadata
