"""Query history routes."""
from fastapi import APIRouter, Query
from datetime import datetime, timedelta
from typing import List

from app.models.schemas import QueryHistory, HistoryResponse
from app.utils.logger import logger

# In-memory history storage (use database in production)
query_history: List[QueryHistory] = []

router = APIRouter(prefix="/api/v1/history", tags=["history"])


@router.get("/queries", response_model=HistoryResponse)
async def get_query_history(
    limit: int = Query(50, ge=1, le=500),
    query_type: str = Query(None),
    success_only: bool = Query(False),
) -> HistoryResponse:
    """
    Get query execution history.

    Args:
        limit: Maximum number of queries to return
        query_type: Filter by query type (SELECT, INSERT, UPDATE, DELETE)
        success_only: Return only successful queries

    Returns:
        Query history
    """
    filtered_history = query_history

    # Filter by query type
    if query_type:
        filtered_history = [q for q in filtered_history if q.query_type == query_type]

    # Filter by success
    if success_only:
        filtered_history = [q for q in filtered_history if q.success]

    # Sort by timestamp (newest first) and limit
    filtered_history = sorted(filtered_history, key=lambda x: x.timestamp, reverse=True)[:limit]

    return HistoryResponse(
        success=True,
        total=len(filtered_history),
        history=filtered_history,
    )


@router.get("/statistics")
async def get_history_statistics() -> dict:
    """
    Get statistics about query history.

    Returns:
        History statistics
    """
    total_queries = len(query_history)
    successful_queries = len([q for q in query_history if q.success])
    failed_queries = total_queries - successful_queries

    # Count by type
    type_counts = {}
    for query in query_history:
        query_type = query.query_type
        type_counts[query_type] = type_counts.get(query_type, 0) + 1

    # Average execution time
    avg_execution_time = (
        sum(q.execution_time_ms for q in query_history) / total_queries if total_queries > 0 else 0
    )

    return {
        "success": True,
        "total_queries": total_queries,
        "successful_queries": successful_queries,
        "failed_queries": failed_queries,
        "success_rate": (successful_queries / total_queries * 100) if total_queries > 0 else 0,
        "average_execution_time_ms": avg_execution_time,
        "queries_by_type": type_counts,
    }


@router.delete("/clear")
async def clear_history() -> dict:
    """
    Clear query history.

    Returns:
        Confirmation
    """
    global query_history
    query_history = []
    logger.info("Query history cleared")
    return {
        "success": True,
        "message": "Query history cleared",
    }


@router.post("/add")
async def add_to_history(
    query: str,
    query_type: str,
    execution_time_ms: float,
    success: bool,
    rows_affected: int = 0,
) -> dict:
    """
    Add query to history (called internally).

    Args:
        query: SQL query
        query_type: Query type
        execution_time_ms: Execution time in milliseconds
        success: Whether query was successful
        rows_affected: Number of rows affected

    Returns:
        Confirmation
    """
    from datetime import datetime

    history_entry = QueryHistory(
        id=f"query_{datetime.now().timestamp()}",
        query=query,
        query_type=query_type,
        timestamp=datetime.now().isoformat(),
        execution_time_ms=execution_time_ms,
        success=success,
        rows_affected=rows_affected,
    )

    query_history.append(history_entry)
    logger.info(f"Query added to history: {query_type}")

    return {
        "success": True,
        "message": "Query added to history",
    }
