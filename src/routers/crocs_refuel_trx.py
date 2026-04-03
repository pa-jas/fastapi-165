"""Crocs Refuel Trx router"""

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text

from src.config.auth import verify_credentials
from src.config.database import crocs_engine
from src.routers.date_filters import build_date_where_clause

router = APIRouter(prefix="/api/crocs/refuel-trx", tags=["CrocsRefuelTrx"])


@router.get("", response_model=Dict[str, Any])
async def get_refuel_trx(
    date_from: Optional[str] = Query(default=None, description="Start date filter (YYYY-MM-DD format)"),
    date_to: Optional[str] = Query(default=None, description="End date filter (YYYY-MM-DD format)"),
    current_user: dict = Depends(verify_credentials),
):
    """
    Get all data from crocs.REFUEL_TRX table with optional TRX_DATE date filtering.

    - **date_from**: Start date filter in YYYY-MM-DD format (optional)
    - **date_to**: End date filter in YYYY-MM-DD format (optional)

    Example: `/api/crocs/refuel-trx?date_from=2025-01-01&date_to=2025-01-31`
    """

    try:
        with crocs_engine.connect() as conn:
            where_clause, params = build_date_where_clause(
                date_from=date_from,
                date_to=date_to,
                column_name="TRX_DATE",
            )

            count_query = f"SELECT COUNT(*) as total FROM crocs.stg.REFUEL_TRX {where_clause}"
            count_result = conn.execute(text(count_query), params)
            total = count_result.fetchone()[0]

            query = text(f"""
                SELECT *
                FROM crocs.stg.REFUEL_TRX
                {where_clause}
                ORDER BY TRX_DATE DESC
            """)

            result = conn.execute(query, params)
            columns = result.keys()
            rows = result.fetchall()

            data = [dict(zip(columns, row)) for row in rows]

            return {
                "total": total,
                "date_from": date_from,
                "date_to": date_to,
                "data": data,
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/count")
async def get_refuel_trx_count(
    date_from: Optional[str] = Query(default=None, description="Start date filter (YYYY-MM-DD format)"),
    date_to: Optional[str] = Query(default=None, description="End date filter (YYYY-MM-DD format)"),
    current_user: dict = Depends(verify_credentials),
):
    """
    Get total count of records in crocs.REFUEL_TRX table with optional TRX_DATE filtering.
    """
    try:
        with crocs_engine.connect() as conn:
            where_clause, params = build_date_where_clause(
                date_from=date_from,
                date_to=date_to,
                column_name="TRX_DATE",
            )

            query = f"SELECT COUNT(*) as total FROM crocs.stg.REFUEL_TRX {where_clause}"
            result = conn.execute(text(query), params)
            total = result.fetchone()[0]

            return {
                "total": total,
                "date_from": date_from,
                "date_to": date_to,
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

