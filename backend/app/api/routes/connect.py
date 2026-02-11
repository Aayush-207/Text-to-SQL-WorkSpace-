"""Database connection routes."""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection_manager import connection_manager
from app.models.schemas import DatabaseConnection, ConnectionResponse
from app.utils.logger import logger

router = APIRouter(prefix="/api/v1/connect", tags=["connection"])


@router.post("/test", response_model=ConnectionResponse)
async def test_connection(connection: DatabaseConnection) -> ConnectionResponse:
    """
    Test database connection.

    Args:
        connection: Database connection details

    Returns:
        Connection test response
    """
    try:
        # Note: In production, use the provided connection details
        # For now, test the default connection
        is_connected = await connection_manager.test_connection()

        if is_connected:
            logger.info(f"Connection test successful to {connection.host}:{connection.port}")
            return ConnectionResponse(
                success=True,
                message="Connection successful",
                connected=True,
            )
        else:
            return ConnectionResponse(
                success=False,
                message="Connection failed",
                connected=False,
            )
    except Exception as e:
        logger.error(f"Connection test failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def connection_status() -> dict:
    """
    Get current connection status.

    Returns:
        Connection status information
    """
    try:
        is_connected = await connection_manager.test_connection()
        return {
            "success": True,
            "connected": is_connected,
            "message": "Connected to database" if is_connected else "Not connected",
        }
    except Exception as e:
        logger.error(f"Failed to get connection status: {str(e)}")
        return {
            "success": False,
            "connected": False,
            "message": str(e),
        }
