"""SQL generation routes."""
from fastapi import APIRouter, HTTPException

from app.db.connection_manager import connection_manager
from app.db.metadata_service import MetadataService
from app.ai.sql_generator import sql_generator
from app.models.schemas import GenerateSQLRequest, GenerateSQLResponse
from app.utils.logger import logger

router = APIRouter(prefix="/api/v1/generate", tags=["sql_generation"])


@router.post("/sql", response_model=GenerateSQLResponse)
async def generate_sql(request: GenerateSQLRequest) -> GenerateSQLResponse:
    """
    Generate SQL from natural language query.

    Args:
        request: Generation request with natural language query

    Returns:
        Generated SQL query with metadata
    """
    try:
        # Get schema metadata
        async with connection_manager.get_session() as session:
            metadata = await MetadataService.get_schema_metadata(session, request.schema)

        # Generate SQL
        result = await sql_generator.generate_sql(request.natural_language_query, metadata)

        if result["success"]:
            return GenerateSQLResponse(
                success=True,
                sql=result["sql"],
                type=result["type"],
                confidence=result["confidence"],
                explanation=result["explanation"],
            )
        else:
            return GenerateSQLResponse(
                success=False,
                error=result.get("error", "Failed to generate SQL"),
            )

    except Exception as e:
        logger.error(f"Failed to generate SQL: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/available-models")
async def get_available_models() -> dict:
    """
    Get available AI models.

    Returns:
        List of available models
    """
    return {
        "success": True,
        "models": [
            {
                "id": "gemini-2.0-flash",
                "name": "Gemini 2.0 Flash",
                "description": "Fast and efficient model for SQL generation",
            },
        ],
    }
