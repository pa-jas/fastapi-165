"""
FastAPI Main Application

This is the main entry point for the FastAPI application.
To add a new API, create a router file in routers/ and include it here.
"""
from fastapi import FastAPI
from src.routers import auth, data_tables, health

# Create FastAPI app
app = FastAPI(
    title="FastAPI Application",
    description="A scalable FastAPI application with PostgreSQL database connection and HTTP Basic Authentication",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to FastAPI in Docker!",
        "docs": "/docs",
        "health": "/health",
        "auth": "Use HTTP Basic Auth (username/password) for protected endpoints"
    }


# Include routers
app.include_router(health.router)  # Public endpoint
app.include_router(auth.router)    # Authentication endpoints
app.include_router(data_tables.router)  # Config-driven table endpoints (protected)

# To add a new table API: edit src/routers/data_tables.py (TABLE_ENDPOINTS).
# For other routers: add a module under routers/ and include_router here.
