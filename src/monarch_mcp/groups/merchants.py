from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP
from monarch_api import (
    MerchantSort,
    delete_merchant as api_delete_merchant,
    get_merchant as api_get_merchant,
    list_merchants as api_list_merchants,
    update_merchant as api_update_merchant,
)

from monarch_mcp.serialization import to_jsonable
from monarch_mcp.session import require_session


def list_merchants(
    *,
    search: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    sort: str = "TRANSACTION_COUNT",
    session_path: str | None = None,
) -> Any:
    return to_jsonable(
        api_list_merchants(
            require_session(session_path),
            search=search,
            limit=limit,
            offset=offset,
            sort=MerchantSort(sort),
        )
    )


def get_merchant(merchant_id: str, *, session_path: str | None = None) -> Any:
    return to_jsonable(api_get_merchant(require_session(session_path), merchant_id))


def update_merchant(
    merchant_id: str,
    *,
    name: str | None = None,
    session_path: str | None = None,
) -> Any:
    return to_jsonable(
        api_update_merchant(require_session(session_path), merchant_id, name=name)
    )


def delete_merchant(
    merchant_id: str,
    *,
    move_to_merchant_id: str | None = None,
    session_path: str | None = None,
) -> Any:
    return to_jsonable(
        api_delete_merchant(
            require_session(session_path),
            merchant_id,
            move_to_merchant_id=move_to_merchant_id,
        )
    )


def register(mcp: FastMCP) -> None:
    mcp.tool(name="merchants_list_merchants")(list_merchants)
    mcp.tool(name="merchants_get_merchant")(get_merchant)
    mcp.tool(name="merchants_update_merchant")(update_merchant)
    mcp.tool(name="merchants_delete_merchant")(delete_merchant)
