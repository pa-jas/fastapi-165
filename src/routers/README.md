# How to Add a New API Router

This directory contains all API routers. Each router is a separate file that can be easily added or removed.

## Quick Steps to Add a New API

### Step 1: Create a New Router File

Create a new Python file in this directory (e.g., `my_table.py`):

```python
from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from typing import Dict, Any
from config.database import engine

# Create router with prefix and tags
router = APIRouter(prefix="/api/my_table", tags=["MyTable"])

@router.get("")
async def get_all():
    """Get all records from your table"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM your_table LIMIT 100"))
            columns = result.keys()
            rows = result.fetchall()
            data = [dict(zip(columns, row)) for row in rows]
            return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}")
async def get_by_id(id: int):
    """Get a single record by ID"""
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM your_table WHERE id = :id"),
                {"id": id}
            )
            row = result.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Not found")
            columns = result.keys()
            return dict(zip(columns, row))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Step 2: Register the Router in main.py

Open `src/main.py` and add:

```python
from routers import my_table  # Add this import

# ... existing code ...

app.include_router(my_table.router)  # Add this line
```

### Step 3: Test Your API

1. Restart the application
2. Visit http://localhost:8000/docs to see your new endpoints
3. Test the endpoints

## Tips

- Use the `example.py` file as a template
- Each router should have a unique `prefix` (e.g., `/api/table_name`)
- Add descriptive `tags` for better API documentation
- Always handle exceptions properly
- Use type hints for better code clarity

## Example Router Structure

```python
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import text
from config.database import engine

router = APIRouter(prefix="/api/your_table", tags=["YourTable"])

@router.get("")
async def get_all(limit: int = 100, offset: int = 0):
    # Your logic here
    pass

@router.get("/count")
async def get_count():
    # Your logic here
    pass
```
