"""Diff service for comparing data changes."""
from typing import Any, Dict, List
from app.utils.logger import logger


class DiffService:
    """Service for comparing before/after data."""

    @staticmethod
    def calculate_row_diff(
        before_rows: List[Dict[str, Any]],
        after_rows: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Calculate differences between before and after rows.

        Args:
            before_rows: Rows before query execution
            after_rows: Rows after query execution

        Returns:
            Dictionary with diff information
        """
        # Convert rows to sets of tuples for comparison
        before_set = {tuple(sorted(row.items())) for row in before_rows}
        after_set = {tuple(sorted(row.items())) for row in after_rows}

        added = list(after_set - before_set)
        removed = list(before_set - after_set)

        return {
            "rows_added": len(added),
            "rows_removed": len(removed),
            "rows_unchanged": len(before_set & after_set),
            "added_rows": [dict(row) for row in added[:10]],  # Limit display
            "removed_rows": [dict(row) for row in removed[:10]],  # Limit display
        }

    @staticmethod
    def generate_diff_summary(
        rows_added: int,
        rows_removed: int,
        rows_modified: int = 0,
    ) -> str:
        """
        Generate human-readable diff summary.

        Args:
            rows_added: Number of rows added
            rows_removed: Number of rows removed
            rows_modified: Number of rows modified

        Returns:
            Formatted summary string
        """
        summary_parts = []

        if rows_added > 0:
            summary_parts.append(f"+{rows_added} rows added")
        if rows_removed > 0:
            summary_parts.append(f"-{rows_removed} rows removed")
        if rows_modified > 0:
            summary_parts.append(f"~{rows_modified} rows modified")

        if not summary_parts:
            return "No changes"

        return ", ".join(summary_parts)

    @staticmethod
    def compare_column_changes(
        before_rows: List[Dict[str, Any]],
        after_rows: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Analyze changes at column level.

        Args:
            before_rows: Rows before query execution
            after_rows: Rows after query execution

        Returns:
            Dictionary with column-level changes
        """
        changes: Dict[str, Dict[str, Any]] = {}

        if not before_rows or not after_rows:
            return changes

        # Get all columns
        all_columns = set()
        for row in before_rows + after_rows:
            all_columns.update(row.keys())

        # Analyze changes per column
        for column in all_columns:
            before_values = [row.get(column) for row in before_rows if column in row]
            after_values = [row.get(column) for row in after_rows if column in row]

            if before_values != after_values:
                changes[column] = {
                    "before": before_values[:5],  # Limit to 5 examples
                    "after": after_values[:5],
                    "changed": True,
                }

        return changes
