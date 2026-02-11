"""FastAPI application main entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.db.connection_manager import connection_manager
from app.utils.logger import logger

# Import routes
from app.api.routes import connect, schema, generate_sql, preview, execute, history

# Settings
settings = get_settings()


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifespan.

    - Startup: Initialize database connection
    - Shutdown: Close database connection
    """
    # Startup
    logger.info("Starting up Text to SQL API...")
    await connection_manager.initialize()
    await connection_manager.test_connection()
    logger.info("Database connection initialized")

    yield

    # Shutdown
    logger.info("Shutting down Text to SQL API...")
    await connection_manager.close()
    logger.info("Database connection closed")


# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else None,
        },
    )


# Health check endpoint
@app.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint.

    Returns:
        Health status
    """
    try:
        is_connected = await connection_manager.test_connection()
        return {
            "status": "healthy" if is_connected else "unhealthy",
            "database_connected": is_connected,
            "api_version": settings.api_version,
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "database_connected": False,
            "error": str(e),
        }


# Root endpoint
@app.get("/")
async def root() -> dict:
    """Root endpoint with API information."""
    return {
        "name": settings.api_title,
        "version": settings.api_version,
        "description": settings.api_description,
        "docs": "/docs",
        "health": "/health",
    }


# Include routes
app.include_router(connect.router)
app.include_router(schema.router)
app.include_router(generate_sql.router)
app.include_router(preview.router)
app.include_router(execute.router)
app.include_router(history.router)


# API documentation
@app.get("/api/v1/docs")
async def get_api_docs() -> dict:
    """Get API documentation."""
    return {
        "title": "Text to SQL API",
        "version": settings.api_version,
        "endpoints": {
            "connection": {
                "POST /api/v1/connect/test": "Test database connection",
                "GET /api/v1/connect/status": "Get connection status",
            },
            "schema": {
                "GET /api/v1/schema/metadata": "Get schema metadata",
                "GET /api/v1/schema/tables": "Get list of tables",
                "GET /api/v1/schema/columns": "Get column information",
                "GET /api/v1/schema/foreign-keys": "Get foreign key relationships",
                "GET /api/v1/schema/indexes": "Get database indexes",
                "GET /api/v1/schema/sample-data": "Get sample data from table",
            },
            "sql_generation": {
                "POST /api/v1/generate/sql": "Generate SQL from natural language",
            },
            "preview": {
                "POST /api/v1/preview/execute": "Preview query execution",
                "POST /api/v1/preview/simulate": "Simulate query execution",
            },
            "execution": {
                "POST /api/v1/execute/query": "Execute SQL query",
                "POST /api/v1/execute/batch": "Execute multiple queries",
                "POST /api/v1/execute/explain": "Explain query metadata",
            },
            "history": {
                "GET /api/v1/history/queries": "Get query history",
                "GET /api/v1/history/statistics": "Get history statistics",
                "DELETE /api/v1/history/clear": "Clear query history",
            },
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
