"""
Example router template - Copy this file to create a new API router

To use this template:
1. Copy this file to a new file (e.g., my_new_api.py)
2. Rename the router variable and update the prefix
3. Add your endpoints
4. Import and include the router in main.py
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from config.database import engine
from sqlalchemy import text

# Create a new router with a prefix
router = APIRouter(prefix="/api/example", tags=["Example"])


@router.get("")
async def get_example():
    """
    Example endpoint - GET all records
    
    Replace this with your actual endpoint logic
    """
    try:
        # Example: Query a table
        # with engine.connect() as conn:
        #     result = conn.execute(text("SELECT * FROM your_table LIMIT 10"))
        #     columns = result.keys()
        #     rows = result.fetchall()
        #     data = [dict(zip(columns, row)) for row in rows]
        #     return {"data": data}
        
        return {"message": "This is an example endpoint"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )


@router.get("/{item_id}")
async def get_example_item(item_id: int):
    """
    Example endpoint - GET single record by ID
    
    Replace this with your actual endpoint logic
    """
    try:
        # Example: Query a single record
        # with engine.connect() as conn:
        #     result = conn.execute(
        #         text("SELECT * FROM your_table WHERE id = :id"),
        #         {"id": item_id}
        #     )
        #     row = result.fetchone()
        #     if not row:
        #         raise HTTPException(status_code=404, detail="Item not found")
        #     columns = result.keys()
        #     return dict(zip(columns, row))
        
        return {"item_id": item_id, "message": "Example item"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )
