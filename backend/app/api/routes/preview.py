"""Query preview routes."""
from fastapi import APIRouter, HTTPException

from app.db.connection_manager import connection_manager
from app.services.preview_service import PreviewService
from app.models.schemas import PreviewRequest, PreviewResponse
from app.utils.logger import logger

router = APIRouter(prefix="/api/v1/preview", tags=["preview"])


@router.post("/execute", response_model=PreviewResponse)
async def preview_query(request: PreviewRequest) -> PreviewResponse:
    """
    Preview query execution without permanent changes.

    Args:
        request: Preview request with SQL query

    Returns:
        Preview of query results
    """
    try:
        async with connection_manager.get_session() as session:
            result = await PreviewService.preview_with_limit(
                session,
                request.sql,
                limit=request.limit,
            )

            if result["success"]:
                return PreviewResponse(
                    success=True,
                    query_type=result.get("query_type"),
                    preview_rows=result.get("preview_rows", []),
                    affected_rows=result.get("affected_rows", 0),
                )
            else:
                return PreviewResponse(
                    success=False,
                    error=result.get("error", "Failed to preview query"),
                )

    except Exception as e:
        logger.error(f"Failed to preview query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/simulate")
async def simulate_execution(request: PreviewRequest) -> dict:
    """
    Simulate query execution showing affected rows.

    Args:
        request: Preview request

    Returns:
        Simulation results
    """
    try:
        async with connection_manager.get_session() as session:
            result = await PreviewService.preview_query(session, request.sql)

            return {
                "success": result["success"],
                "query_type": result.get("query_type"),
                "affected_rows": result.get("affected_rows", 0),
                "preview_rows": result.get("preview_rows", []),
                "message": f"Query would affect {result.get('affected_rows', 0)} rows",
                "error": result.get("error"),
            }

    except Exception as e:
        logger.error(f"Failed to simulate execution: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
