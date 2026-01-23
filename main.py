"""
FastAPI Main Application

This is the main entry point for the FastAPI application.
To add a new API, create a router file in routers/ and include it here.
"""
from fastapi import FastAPI
from routers import health, jasdatadaily, auth

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
app.include_router(jasdatadaily.router)  # Protected endpoints

# To add a new API router:
# 1. Create a new file in routers/ (e.g., routers/my_new_api.py)
# 2. Import it above (e.g., from routers import my_new_api)
# 3. Include it here (e.g., app.include_router(my_new_api.router))
