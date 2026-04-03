"""
Config-driven table listing endpoints.

Add a TableEndpointSpec below for each API; set engine, FROM clause,
date filtering, and ordering in one place.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.engine import Engine

from src.config.auth import verify_credentials
from src.config.database import crocs_engine, dwh_engine
from src.routers.date_filters import build_date_where_clause

EngineName = Literal["dwh", "crocs"]

_ENGINES: dict[EngineName, Engine] = {
    "dwh": dwh_engine,
    "crocs": crocs_engine,
}


@dataclass(frozen=True)
class TableEndpointSpec:
    """Describes one GET endpoint that returns all rows from a table."""

    path: str
    tags: list[str]
    engine_name: EngineName
    # Trusted SQL fragment, e.g. main.jasdatadaily or stg."REFUEL_TRX"
    from_sql: str
    use_date_filter: bool
    # Use quoted identifiers when the DB column is case-sensitive, e.g. '"TRX_DATE"'
    date_column: Optional[str] = None
    order_by_column: Optional[str] = None

    def __post_init__(self) -> None:
        if self.use_date_filter and not self.date_column:
            raise ValueError(f"{self.path}: date_column is required when use_date_filter is True")


# --- Register endpoints here ---
TABLE_ENDPOINTS: list[TableEndpointSpec] = [
    TableEndpointSpec(
        path="/api/jasdatadaily",
        tags=["JasDataDaily"],
        engine_name="dwh",
        from_sql="main.jasdatadaily",
        use_date_filter=True,
        date_column="date",
        order_by_column="date",
    ),
    TableEndpointSpec(
        path="/api/crocs/refuel-trx",
        tags=["CrocsRefuelTrx"],
        engine_name="crocs",
        from_sql='stg."REFUEL_TRX"',
        use_date_filter=True,
        # Quoted so PostgreSQL keeps uppercase (matches select "TRX_DATE" from ...)
        date_column='"TRX_DATE"',
        order_by_column='"TRX_DATE"',
    ),
]


async def _execute_table_query(
    spec: TableEndpointSpec,
    date_from: Optional[str],
    date_to: Optional[str],
) -> Dict[str, Any]:
    engine = _ENGINES[spec.engine_name]
    try:
        with engine.connect() as conn:
            if spec.use_date_filter:
                assert spec.date_column is not None
                where_clause, params = build_date_where_clause(
                    date_from=date_from,
                    date_to=date_to,
                    column_name=spec.date_column,
                )
            else:
                where_clause, params = "", {}

            order_col = spec.order_by_column or (
                spec.date_column if spec.use_date_filter else None
            )
            order_sql = f" ORDER BY {order_col} DESC" if order_col else ""

            query = text(f"SELECT * FROM {spec.from_sql} {where_clause}{order_sql}")
            result = conn.execute(query, params)
            columns = result.keys()
            rows = result.fetchall()
            data = [dict(zip(columns, row)) for row in rows]

            return {
                "date_from": date_from,
                "date_to": date_to,
                "data": data,
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}",
        )


def _build_router() -> APIRouter:
    api = APIRouter()

    for spec in TABLE_ENDPOINTS:
        if spec.use_date_filter:

            async def dated_handler(
                date_from: Optional[str] = Query(
                    default=None,
                    description="Start date filter (YYYY-MM-DD format)",
                ),
                date_to: Optional[str] = Query(
                    default=None,
                    description="End date filter (YYYY-MM-DD format)",
                ),
                current_user: dict = Depends(verify_credentials),
                _spec: TableEndpointSpec = spec,
            ) -> Dict[str, Any]:
                return await _execute_table_query(_spec, date_from, date_to)

            safe = spec.path.strip("/").replace("/", "_")
            dated_handler.__name__ = f"get_table_{safe}"

            api.add_api_route(
                spec.path,
                dated_handler,
                methods=["GET"],
                tags=spec.tags,
                response_model=Dict[str, Any],
            )
        else:

            async def plain_handler(
                current_user: dict = Depends(verify_credentials),
                _spec: TableEndpointSpec = spec,
            ) -> Dict[str, Any]:
                return await _execute_table_query(_spec, None, None)

            safe = spec.path.strip("/").replace("/", "_")
            plain_handler.__name__ = f"get_table_{safe}"

            api.add_api_route(
                spec.path,
                plain_handler,
                methods=["GET"],
                tags=spec.tags,
                response_model=Dict[str, Any],
            )

    return api


router = _build_router()
