"""JasDataDaily router"""
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy import text
from typing import Any, Dict, Optional

from src.config.database import dwh_engine
from src.config.auth import verify_credentials
from src.routers.date_filters import build_date_where_clause

router = APIRouter(prefix="/api/jasdatadaily", tags=["JasDataDaily"])


@router.get("", response_model=Dict[str, Any])
async def get_jasdatadaily(
    date_from: Optional[str] = Query(default=None, description="Start date filter (YYYY-MM-DD format)"),
    date_to: Optional[str] = Query(default=None, description="End date filter (YYYY-MM-DD format)"),
    current_user: dict = Depends(verify_credentials)
):
    """
    Get all data from main.jasdatadaily table with optional date filtering
    
    - **date_from**: Start date filter in YYYY-MM-DD format (optional)
    - **date_to**: End date filter in YYYY-MM-DD format (optional)
    
    Example: `/api/jasdatadaily?date_from=2025-01-01&date_to=2025-01-31`
    """
    try:
        with dwh_engine.connect() as conn:
            # Build WHERE clause based on date parameters
            where_clause, params = build_date_where_clause(
                date_from=date_from,
                date_to=date_to,
                column_name="date",
            )
            
            # Get total count with date filter
            count_query = f"SELECT COUNT(*) as total FROM main.jasdatadaily {where_clause}"
            count_result = conn.execute(text(count_query), params)
            total = count_result.fetchone()[0]
            
            # Get all data with date filter (no limit)
            query = text(f"""
                SELECT * FROM main.jasdatadaily 
                {where_clause}
                ORDER BY date DESC
            """)
            
            result = conn.execute(query, params)
            
            # Get column names
            columns = result.keys()
            
            # Fetch all rows
            rows = result.fetchall()
            
            # Convert to list of dictionaries
            data = [dict(zip(columns, row)) for row in rows]
            
            return {
                "total": total
            }
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )


@router.get("/count")
async def get_jasdatadaily_count(
    date_from: Optional[str] = Query(default=None, description="Start date filter (YYYY-MM-DD format)"),
    date_to: Optional[str] = Query(default=None, description="End date filter (YYYY-MM-DD format)"),
    current_user: dict = Depends(verify_credentials)
):
    """
    Get total count of records in main.jasdatadaily table with optional date filtering
    
    - **date_from**: Start date filter in YYYY-MM-DD format (optional)
    - **date_to**: End date filter in YYYY-MM-DD format (optional)
    """
    try:
        with dwh_engine.connect() as conn:
            # Build WHERE clause based on date parameters
            where_clause, params = build_date_where_clause(
                date_from=date_from,
                date_to=date_to,
                column_name="date",
            )
            
            query = f"SELECT COUNT(*) as total FROM main.jasdatadaily {where_clause}"
            result = conn.execute(text(query), params)
            total = result.fetchone()[0]
            return {
                "total": total,
                "date_from": date_from,
                "date_to": date_to
            }
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
