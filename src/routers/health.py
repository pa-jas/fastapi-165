"""Health check router"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text
from config.database import engine

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health():
    """Health check endpoint"""
    try:
        # Test database connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return JSONResponse(
            status_code=200,
            content={"status": "healthy", "database": "connected"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "disconnected", "error": str(e)}
        )
