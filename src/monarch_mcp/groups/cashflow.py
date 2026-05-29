from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP
from monarch_api import (
    CashflowBreakdownDirection,
    CashflowBreakdownGroup,
    CashflowInterval,
    get_cashflow_breakdown as api_get_cashflow_breakdown,
    get_cashflow_summary as api_get_cashflow_summary,
    get_cashflow_trends as api_get_cashflow_trends,
)

from monarch_mcp.converters import cashflow_filter
from monarch_mcp.serialization import to_jsonable
from monarch_mcp.session import require_session
from monarch_mcp.tool_metadata import register_api_tool


def get_cashflow_summary(
    start_date: str,
    end_date: str,
    *,
    filters: dict[str, Any] | None = None,
    session_path: str | None = None,
) -> Any:
    return to_jsonable(
        api_get_cashflow_summary(
            require_session(session_path),
            start_date,
            end_date,
            filters=cashflow_filter(filters),
        )
    )


def get_cashflow_trends(
    start_date: str,
    end_date: str,
    *,
    interval: str = "month",
    filters: dict[str, Any] | None = None,
    session_path: str | None = None,
) -> Any:
    return to_jsonable(
        api_get_cashflow_trends(
            require_session(session_path),
            start_date,
            end_date,
            interval=CashflowInterval(interval),
            filters=cashflow_filter(filters),
        )
    )


def get_cashflow_breakdown(
    start_date: str,
    end_date: str,
    direction: str,
    *,
    group_by: str = "category",
    filters: dict[str, Any] | None = None,
    session_path: str | None = None,
) -> Any:
    return to_jsonable(
        api_get_cashflow_breakdown(
            require_session(session_path),
            start_date,
            end_date,
            CashflowBreakdownDirection(direction),
            group_by=CashflowBreakdownGroup(group_by),
            filters=cashflow_filter(filters),
        )
    )


def register(mcp: FastMCP) -> None:
    register_api_tool(mcp, "cashflow", "get_cashflow_summary", get_cashflow_summary)
    register_api_tool(mcp, "cashflow", "get_cashflow_trends", get_cashflow_trends)
    register_api_tool(
        mcp,
        "cashflow",
        "get_cashflow_breakdown",
        get_cashflow_breakdown,
    )
