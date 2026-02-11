"""Query execution routes."""
from fastapi import APIRouter, HTTPException

from app.db.connection_manager import connection_manager
from app.db.query_executor import QueryExecutor
from app.models.schemas import ExecuteQueryRequest, ExecuteQueryResponse
from app.utils.logger import logger

router = APIRouter(prefix="/api/v1/execute", tags=["execution"])


@router.post("/query", response_model=ExecuteQueryResponse)
async def execute_query(request: ExecuteQueryRequest) -> ExecuteQueryResponse:
    """
    Execute SQL query.

    Args:
        request: Execution request with SQL query

    Returns:
        Query execution result
    """
    try:
        async with connection_manager.get_session() as session:
            result = await QueryExecutor.execute_query(session, request.sql)

            if result["success"]:
                if result.get("query_type") == "SELECT":
                    return ExecuteQueryResponse(
                        success=True,
                        query_type=result["query_type"],
                        data=result.get("data", []),
                        rows_returned=result.get("rows_returned", 0),
                    )
                else:
                    return ExecuteQueryResponse(
                        success=True,
                        query_type=result["query_type"],
                        affected_rows=result.get("affected_rows", 0),
                    )
            else:
                return ExecuteQueryResponse(
                    success=False,
                    query_type=result.get("query_type"),
                    error=result.get("error", "Query execution failed"),
                )

    except Exception as e:
        logger.error(f"Failed to execute query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch")
async def execute_batch(requests: list[ExecuteQueryRequest]) -> dict:
    """
    Execute multiple queries in batch.

    Args:
        requests: List of execution requests

    Returns:
        Batch execution results
    """
    results = []
    async with connection_manager.get_session() as session:
        for request in requests:
            result = await QueryExecutor.execute_query(session, request.sql)
            results.append(result)

    return {
        "success": True,
        "total": len(results),
        "results": results,
    }


@router.post("/explain")
async def explain_query(request: ExecuteQueryRequest) -> dict:
    """
    Explain query without executing it.

    Args:
        request: Query to explain

    Returns:
        Query explanation
    """
    try:
        from app.ai.sql_explainer import SQLExplainer

        metadata = SQLExplainer.extract_query_metadata(request.sql)

        return {
            "success": True,
            "query": request.sql,
            "metadata": metadata,
        }

    except Exception as e:
        logger.error(f"Failed to explain query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
