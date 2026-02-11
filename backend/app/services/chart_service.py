"""Chart and visualization data service."""
from typing import Any, Dict, List
from collections import defaultdict
from app.utils.logger import logger


class ChartService:
    """Service for generating chart-ready data from query results."""

    @staticmethod
    def prepare_pie_chart_data(
        rows: List[Dict[str, Any]],
        label_column: str,
        value_column: str,
    ) -> Dict[str, Any]:
        """
        Prepare data for pie chart.

        Args:
            rows: Query result rows
            label_column: Column to use for labels
            value_column: Column to use for values

        Returns:
            Chart data dictionary
        """
        labels = []
        values = []

        for row in rows:
            if label_column in row and value_column in row:
                labels.append(str(row[label_column]))
                values.append(float(row[value_column]) if isinstance(row[value_column], (int, float)) else 0)

        return {
            "type": "pie",
            "labels": labels,
            "datasets": [{"data": values, "backgroundColor": ChartService.get_colors(len(labels))}],
        }

    @staticmethod
    def prepare_bar_chart_data(
        rows: List[Dict[str, Any]],
        x_column: str,
        y_columns: List[str],
    ) -> Dict[str, Any]:
        """
        Prepare data for bar chart.

        Args:
            rows: Query result rows
            x_column: Column to use for X-axis
            y_columns: Columns to use for Y-axis values

        Returns:
            Chart data dictionary
        """
        x_labels = []
        datasets = []

        # Extract X labels
        for row in rows:
            if x_column in row:
                x_labels.append(str(row[x_column]))

        # Create datasets for each Y column
        for y_col in y_columns:
            y_values = []
            for row in rows:
                if y_col in row:
                    y_values.append(float(row[y_col]) if isinstance(row[y_col], (int, float)) else 0)
                else:
                    y_values.append(0)

            datasets.append({
                "label": y_col,
                "data": y_values,
                "backgroundColor": ChartService.get_random_color(),
            })

        return {
            "type": "bar",
            "labels": x_labels,
            "datasets": datasets,
        }

    @staticmethod
    def prepare_line_chart_data(
        rows: List[Dict[str, Any]],
        x_column: str,
        y_columns: List[str],
    ) -> Dict[str, Any]:
        """
        Prepare data for line chart.

        Args:
            rows: Query result rows
            x_column: Column to use for X-axis
            y_columns: Columns to use for Y-axis values

        Returns:
            Chart data dictionary
        """
        x_labels = []
        datasets = []

        # Extract X labels
        for row in rows:
            if x_column in row:
                x_labels.append(str(row[x_column]))

        # Create datasets for each Y column
        colors = ChartService.get_colors(len(y_columns))
        for idx, y_col in enumerate(y_columns):
            y_values = []
            for row in rows:
                if y_col in row:
                    y_values.append(float(row[y_col]) if isinstance(row[y_col], (int, float)) else 0)
                else:
                    y_values.append(0)

            datasets.append({
                "label": y_col,
                "data": y_values,
                "borderColor": colors[idx],
                "backgroundColor": f"rgba({colors[idx]}, 0.1)",
                "fill": False,
            })

        return {
            "type": "line",
            "labels": x_labels,
            "datasets": datasets,
        }

    @staticmethod
    def prepare_histogram_data(
        rows: List[Dict[str, Any]],
        column: str,
        bins: int = 10,
    ) -> Dict[str, Any]:
        """
        Prepare data for histogram.

        Args:
            rows: Query result rows
            column: Column to use for histogram
            bins: Number of bins

        Returns:
            Chart data dictionary
        """
        values = []
        for row in rows:
            if column in row:
                try:
                    values.append(float(row[column]))
                except (ValueError, TypeError):
                    pass

        if not values:
            return {"type": "histogram", "labels": [], "datasets": []}

        # Calculate bin boundaries
        min_val = min(values)
        max_val = max(values)
        bin_width = (max_val - min_val) / bins

        # Create bins
        bin_counts = defaultdict(int)
        bin_labels = []

        for i in range(bins):
            bin_start = min_val + (i * bin_width)
            bin_end = bin_start + bin_width
            bin_labels.append(f"{bin_start:.2f}-{bin_end:.2f}")

            # Count values in this bin
            for val in values:
                if bin_start <= val < bin_end or (i == bins - 1 and val == max_val):
                    bin_counts[i] += 1

        return {
            "type": "bar",
            "labels": bin_labels,
            "datasets": [
                {
                    "label": f"{column} Distribution",
                    "data": [bin_counts[i] for i in range(bins)],
                    "backgroundColor": "rgba(75, 192, 192, 0.5)",
                }
            ],
        }

    @staticmethod
    def get_colors(count: int) -> List[str]:
        """Get list of colors for charts."""
        colors = [
            "rgb(255, 99, 132)",
            "rgb(54, 162, 235)",
            "rgb(255, 206, 86)",
            "rgb(75, 192, 192)",
            "rgb(153, 102, 255)",
            "rgb(255, 159, 64)",
            "rgb(199, 199, 199)",
            "rgb(83, 102, 255)",
            "rgb(255, 99, 255)",
            "rgb(99, 255, 132)",
        ]
        return (colors * ((count // len(colors)) + 1))[:count]

    @staticmethod
    def get_random_color() -> str:
        """Get random color."""
        import random

        return f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})"

    @staticmethod
    def detect_chart_type(rows: List[Dict[str, Any]]) -> str:
        """
        Auto-detect appropriate chart type based on data.

        Args:
            rows: Query result rows

        Returns:
            Suggested chart type
        """
        if not rows:
            return "table"

        row = rows[0]
        columns = list(row.keys())

        # More than 2 columns - use table
        if len(columns) > 5:
            return "table"

        # Check if data is numeric
        numeric_count = 0
        for col in columns:
            try:
                float(rows[0][col])
                numeric_count += 1
            except (ValueError, TypeError):
                pass

        # Single numeric column - histogram
        if numeric_count == 1 and len(columns) == 1:
            return "histogram"

        # One categorical, one numeric - bar chart
        if numeric_count >= 1 and len(columns) >= 2:
            return "bar"

        # Two numeric - scatter plot
        if numeric_count == 2:
            return "scatter"

        # Default
        return "table"
