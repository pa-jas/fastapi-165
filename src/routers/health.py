"""Health check router"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text
from src.config.database import dwh_engine
from src.config.database import crocs_engine

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health():
    """Health check endpoint"""
    try:
        # Test database connection
        with dwh_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        with crocs_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return JSONResponse(
            status_code=200,
            content={"status": "healthy", "database": "connected", "databases": ["dwh", "crocs"]}
        )
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "disconnected", "error": str(e), "databases": ["dwh", "crocs"]}
        )
