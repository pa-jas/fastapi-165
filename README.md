# FastAPI Docker Project

A FastAPI application containerized with Docker.

## Quick Start

### Build the Docker image
```bash
docker build -t fastapi-app -f src/Dockerfile src/
```

### Run the container
```bash
docker run -d -p 8000:8000 --name fastapi-container fastapi-app
```

### Access the application
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

### Stop and remove container
```bash
docker stop fastapi-container
docker rm fastapi-container
```

## Authentication

This API uses **HTTP Basic Authentication** with username and password. No tokens needed!

**Documentation:**
- [BASIC_AUTH_GUIDE.md](src/BASIC_AUTH_GUIDE.md) - Complete authentication guide

**Quick Start:**
Simply use username and password with each request:
- **Postman:** Authorization tab → Basic Auth → Enter username/password
- **curl:** `curl -u username:password http://localhost:8000/api/jasdatadaily`
- **Python:** `requests.get(url, auth=("username", "password"))`

**Default Users:**
- Username: `admin`, Password: `admin123`
- Username: `user`, Password: `user123`

⚠️ **Change these passwords in production!**

### Using Postman?

1. Go to **Authorization** tab
2. Select **Type:** `Basic Auth`
3. Enter username and password
4. Done! No tokens needed.

## Endpoints

### Public Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check endpoint (includes database connection status)

### Protected Endpoints (Require Username/Password)
- `GET /api/auth/me` - Get current user info

### Protected Endpoints (Require Authentication)
- `GET /api/jasdatadaily` - Get all data from `main.jasdatadaily` table
  - Query parameters:
    - `date_from` (optional) - Start date filter (YYYY-MM-DD format)
    - `date_to` (optional) - End date filter (YYYY-MM-DD format)
  - Example: `GET /api/jasdatadaily?date_from=2025-01-01&date_to=2025-01-31`
- `GET /api/jasdatadaily/count` - Get total count of records in `main.jasdatadaily` table

## Project Structure

```
src/
├── config/
│   ├── database.py          # Database configuration
│   ├── auth.py              # Authentication utilities (JWT)
│   └── users.py             # User management
├── routers/
│   ├── __init__.py
│   ├── health.py            # Health check endpoints (public)
│   ├── auth.py              # Authentication endpoints
│   ├── jasdatadaily.py      # JasDataDaily API endpoints (protected)
│   └── example.py           # Template for new routers
├── main.py                  # Main application file
├── requirements.txt
├── Dockerfile
└── AUTH_GUIDE.md            # Detailed authentication guide
```

## Adding a New API

To add a new API endpoint, simply:

1. **Create a new router file** in `src/routers/` (e.g., `my_new_api.py`)
   - Copy `routers/example.py` as a template
   - Update the router prefix and tags
   - Add your endpoints

2. **Import and include the router** in `src/main.py`:
   ```python
   from routers import my_new_api
   app.include_router(my_new_api.router)
   ```

That's it! Your new API will be automatically available and documented.

### Example: Creating a New API

```python
# src/routers/products.py
from fastapi import APIRouter
from config.database import engine
from sqlalchemy import text

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("")
async def get_products():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM products"))
        # ... your logic
    return {"data": []}
```

Then in `main.py`:
```python
from routers import products
app.include_router(products.router)
```

## Development

To run locally without Docker:
```bash
cd src
pip install -r requirements.txt
uvicorn main:app --reload
```

## Protecting New Endpoints

To protect a new endpoint with authentication, add the `verify_token` dependency:

```python
from fastapi import Depends
from config.auth import verify_token

@router.get("/protected")
async def protected_endpoint(current_user: dict = Depends(verify_token)):
    return {"message": f"Hello {current_user['username']}"}
```

See `src/AUTH_GUIDE.md` for complete authentication documentation.
