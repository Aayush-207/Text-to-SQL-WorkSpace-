"""Pydantic models for API requests and responses."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# Connection Models
class DatabaseConnection(BaseModel):
    """Database connection details."""

    host: str = Field(..., description="Database host")
    port: int = Field(5432, description="Database port")
    database: str = Field(..., description="Database name")
    user: str = Field(..., description="Database user")
    password: str = Field(..., description="Database password")


class ConnectionResponse(BaseModel):
    """Response for database connection."""

    success: bool
    message: str
    connected: bool


# Schema Models
class ColumnSchema(BaseModel):
    """Column schema information."""

    name: str
    data_type: str
    is_nullable: bool
    default: Optional[str] = None
    position: int


class TableSchema(BaseModel):
    """Table schema information."""

    name: str
    columns: List[ColumnSchema]
    row_count: Optional[int] = None


class SchemaResponse(BaseModel):
    """Response for schema information."""

    schema: str
    tables: List[Dict[str, Any]]
    columns: Dict[str, List[Dict[str, Any]]]
    foreign_keys: List[Dict[str, Any]]
    constraints: Dict[str, List[Dict[str, Any]]]
    indexes: Dict[str, List[Dict[str, Any]]]


# SQL Generation Models
class GenerateSQLRequest(BaseModel):
    """Request to generate SQL."""

    natural_language_query: str = Field(..., description="Natural language question")
    schema: str = Field("public", description="Database schema")


class GenerateSQLResponse(BaseModel):
    """Response with generated SQL."""

    success: bool
    sql: Optional[str] = None
    type: Optional[str] = None
    confidence: float = 0.0
    explanation: Optional[str] = None
    error: Optional[str] = None


# Preview Models
class PreviewRequest(BaseModel):
    """Request to preview query."""

    sql: str = Field(..., description="SQL query to preview")
    limit: int = Field(100, description="Maximum rows to return")


class PreviewResponse(BaseModel):
    """Response with preview results."""

    success: bool
    query_type: Optional[str] = None
    preview_rows: List[Dict[str, Any]] = []
    affected_rows: int = 0
    error: Optional[str] = None


# Execute Models
class ExecuteQueryRequest(BaseModel):
    """Request to execute query."""

    sql: str = Field(..., description="SQL query to execute")


class ExecuteQueryResponse(BaseModel):
    """Response after executing query."""

    success: bool
    query_type: Optional[str] = None
    data: Optional[List[Dict[str, Any]]] = None
    rows_returned: int = 0
    affected_rows: int = 0
    error: Optional[str] = None


# History Models
class QueryHistory(BaseModel):
    """Query history entry."""

    id: str
    query: str
    query_type: str
    timestamp: str
    execution_time_ms: float
    success: bool
    rows_affected: int


class HistoryResponse(BaseModel):
    """Response with query history."""

    success: bool
    total: int
    history: List[QueryHistory]


# Explanation Models
class ExplainRequest(BaseModel):
    """Request to explain SQL."""

    sql: str = Field(..., description="SQL query to explain")


class ExplainResponse(BaseModel):
    """Response with SQL explanation."""

    success: bool
    explanation: Optional[str] = None
    error: Optional[str] = None


# Optimization Models
class OptimizeRequest(BaseModel):
    """Request to optimize SQL."""

    sql: str = Field(..., description="SQL query to optimize")


class OptimizeResponse(BaseModel):
    """Response with optimization suggestions."""

    success: bool
    issues: List[str] = []
    optimizations: List[str] = []
    suggested_query: Optional[str] = None
    error: Optional[str] = None


# Chart Models
class ChartRequest(BaseModel):
    """Request to generate chart data."""

    rows: List[Dict[str, Any]] = Field(..., description="Data rows")
    chart_type: str = Field(..., description="Chart type (pie, bar, line, histogram)")
    x_column: Optional[str] = None
    y_columns: Optional[List[str]] = None
    label_column: Optional[str] = None
    value_column: Optional[str] = None


class ChartResponse(BaseModel):
    """Response with chart data."""

    success: bool
    chart_type: str
    chart_data: Dict[str, Any]
    error: Optional[str] = None


# Error Models
class ErrorResponse(BaseModel):
    """Standard error response."""

    success: bool = False
    error: str
    detail: Optional[str] = None
