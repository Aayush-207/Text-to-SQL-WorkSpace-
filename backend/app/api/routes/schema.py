"""Database schema routes."""
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection_manager import connection_manager
from app.db.metadata_service import MetadataService
from app.models.schemas import SchemaResponse
from app.utils.logger import logger

router = APIRouter(prefix="/api/v1/schema", tags=["schema"])


@router.get("/metadata")
async def get_schema_metadata(schema: str = Query("public", description="Schema name")) -> dict:
    """
    Get database schema metadata.

    Args:
        schema: Schema name (default: public)

    Returns:
        Schema metadata
    """
    try:
        async with connection_manager.get_session() as session:
            metadata = await MetadataService.get_schema_metadata(session, schema)
            return {
                "success": True,
                "data": metadata,
            }
    except Exception as e:
        logger.error(f"Failed to get schema metadata: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tables")
async def get_tables(schema: str = Query("public", description="Schema name")) -> dict:
    """
    Get all tables in schema.

    Args:
        schema: Schema name

    Returns:
        List of tables
    """
    try:
        async with connection_manager.get_session() as session:
            tables = await MetadataService.get_tables(session, schema)
            return {
                "success": True,
                "schema": schema,
                "tables": tables,
                "count": len(tables),
            }
    except Exception as e:
        logger.error(f"Failed to get tables: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/columns")
async def get_columns(schema: str = Query("public", description="Schema name")) -> dict:
    """
    Get columns for all tables.

    Args:
        schema: Schema name

    Returns:
        Columns grouped by table
    """
    try:
        async with connection_manager.get_session() as session:
            columns = await MetadataService.get_columns(session, schema)
            return {
                "success": True,
                "schema": schema,
                "columns": columns,
            }
    except Exception as e:
        logger.error(f"Failed to get columns: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/foreign-keys")
async def get_foreign_keys(schema: str = Query("public", description="Schema name")) -> dict:
    """
    Get foreign key relationships.

    Args:
        schema: Schema name

    Returns:
        Foreign key relationships
    """
    try:
        async with connection_manager.get_session() as session:
            fks = await MetadataService.get_foreign_keys(session, schema)
            return {
                "success": True,
                "schema": schema,
                "foreign_keys": fks,
                "count": len(fks),
            }
    except Exception as e:
        logger.error(f"Failed to get foreign keys: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/indexes")
async def get_indexes(schema: str = Query("public", description="Schema name")) -> dict:
    """
    Get database indexes.

    Args:
        schema: Schema name

    Returns:
        Indexes grouped by table
    """
    try:
        async with connection_manager.get_session() as session:
            indexes = await MetadataService.get_indexes(session, schema)
            return {
                "success": True,
                "schema": schema,
                "indexes": indexes,
            }
    except Exception as e:
        logger.error(f"Failed to get indexes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sample-data")
async def get_sample_data(
    table: str = Query(..., description="Table name"),
    schema: str = Query("public", description="Schema name"),
    limit: int = Query(5, description="Number of rows to fetch"),
) -> dict:
    """
    Get sample data from table.

    Args:
        table: Table name
        schema: Schema name
        limit: Number of rows to fetch

    Returns:
        Sample data from table
    """
    try:
        async with connection_manager.get_session() as session:
            data = await MetadataService.get_table_sample_data(session, table, schema, limit)
            return {
                "success": True,
                "table": table,
                "schema": schema,
                "data": data,
                "count": len(data),
            }
    except Exception as e:
        logger.error(f"Failed to get sample data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
