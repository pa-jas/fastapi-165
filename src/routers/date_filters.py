"""Shared helpers for router date filtering."""

from datetime import datetime
from typing import Dict, Optional, Tuple

from fastapi import HTTPException


def validate_date_format(date_str: str, param_name: str) -> None:
    """Validate date format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {param_name} format. Expected YYYY-MM-DD format, got: {date_str}",
        )


def validate_date_range(date_from: Optional[str], date_to: Optional[str]) -> None:
    """Validate that date_from is before or equal to date_to."""
    if not (date_from and date_to):
        return

    try:
        from_date = datetime.strptime(date_from, "%Y-%m-%d")
        to_date = datetime.strptime(date_to, "%Y-%m-%d")
        if from_date > to_date:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid date range: "
                    f"date_from ({date_from}) must be before or equal to "
                    f"date_to ({date_to})"
                ),
            )
    except ValueError:
        # Should not happen if validate_date_format was called first.
        return


def build_date_where_clause(
    *,
    date_from: Optional[str],
    date_to: Optional[str],
    column_name: str,
) -> Tuple[str, Dict[str, str]]:
    """
    Build a safe parameterized WHERE clause for date filtering.

    Note: `column_name` must be a trusted constant (not user input).
    """
    if date_from:
        validate_date_format(date_from, "date_from")
    if date_to:
        validate_date_format(date_to, "date_to")
    if date_from and date_to:
        validate_date_range(date_from, date_to)

    where_clause = ""
    params: Dict[str, str] = {}

    if date_from and date_to:
        where_clause = f"WHERE {column_name} >= :date_from AND {column_name} <= :date_to"
        params["date_from"] = date_from
        params["date_to"] = date_to
    elif date_from:
        where_clause = f"WHERE {column_name} >= :date_from"
        params["date_from"] = date_from
    elif date_to:
        where_clause = f"WHERE {column_name} <= :date_to"
        params["date_to"] = date_to

    return where_clause, params

