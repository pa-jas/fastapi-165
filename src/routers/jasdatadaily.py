"""JasDataDaily router"""
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy import text
from typing import Dict, Any, Optional
from datetime import datetime
from src.config.database import engine
from src.config.auth import verify_credentials

router = APIRouter(prefix="/api/jasdatadaily", tags=["JasDataDaily"])


def validate_date_format(date_str: str, param_name: str) -> None:
    """Validate date format (YYYY-MM-DD)"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {param_name} format. Expected YYYY-MM-DD format, got: {date_str}"
        )


def validate_date_range(date_from: Optional[str], date_to: Optional[str]) -> None:
    """Validate that date_from is before or equal to date_to"""
    if date_from and date_to:
        try:
            from_date = datetime.strptime(date_from, "%Y-%m-%d")
            to_date = datetime.strptime(date_to, "%Y-%m-%d")
            if from_date > to_date:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid date range: date_from ({date_from}) must be before or equal to date_to ({date_to})"
                )
        except ValueError:
            # This should not happen if validate_date_format was called first
            pass


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
    # Validate date parameters
    if date_from:
        validate_date_format(date_from, "date_from")
    if date_to:
        validate_date_format(date_to, "date_to")
    if date_from and date_to:
        validate_date_range(date_from, date_to)
    
    try:
        with engine.connect() as conn:
            # Build WHERE clause based on date parameters
            where_clause = ""
            params = {}
            
            if date_from and date_to:
                where_clause = "WHERE date >= :date_from AND date <= :date_to"
                params["date_from"] = date_from
                params["date_to"] = date_to
            elif date_from:
                where_clause = "WHERE date >= :date_from"
                params["date_from"] = date_from
            elif date_to:
                where_clause = "WHERE date <= :date_to"
                params["date_to"] = date_to
            
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
                "total": total,
                "count": len(data),
                "date_from": date_from,
                "date_to": date_to,
                "data": data
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
    # Validate date parameters
    if date_from:
        validate_date_format(date_from, "date_from")
    if date_to:
        validate_date_format(date_to, "date_to")
    if date_from and date_to:
        validate_date_range(date_from, date_to)
    
    try:
        with engine.connect() as conn:
            # Build WHERE clause based on date parameters
            where_clause = ""
            params = {}
            
            if date_from and date_to:
                where_clause = "WHERE date >= :date_from AND date <= :date_to"
                params["date_from"] = date_from
                params["date_to"] = date_to
            elif date_from:
                where_clause = "WHERE date >= :date_from"
                params["date_from"] = date_from
            elif date_to:
                where_clause = "WHERE date <= :date_to"
                params["date_to"] = date_to
            
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
