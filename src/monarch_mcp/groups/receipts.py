from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP
from monarch_api import (
    delete_receipt as api_delete_receipt,
    get_receipt as api_get_receipt,
    get_receipt_settings as api_get_receipt_settings,
    list_receipts as api_list_receipts,
    match_receipt as api_match_receipt,
    unmatch_receipt as api_unmatch_receipt,
    update_receipt as api_update_receipt,
    update_receipt_settings as api_update_receipt_settings,
    upload_receipt as api_upload_receipt,
)

from monarch_mcp.converters import receipt_filter, receipt_line_items
from monarch_mcp.serialization import to_jsonable
from monarch_mcp.session import require_session


def list_receipts(
    *,
    filters: dict[str, Any] | None = None,
    limit: int = 100,
    offset: int = 0,
    session_path: str | None = None,
) -> Any:
    return to_jsonable(
        api_list_receipts(
            require_session(session_path),
            filters=receipt_filter(filters),
            limit=limit,
            offset=offset,
        )
    )


def get_receipt(receipt_id: str, *, session_path: str | None = None) -> Any:
    return to_jsonable(api_get_receipt(require_session(session_path), receipt_id))


def upload_receipt(
    file_path: str,
    *,
    filename: str | None = None,
    content_type: str | None = None,
    session_path: str | None = None,
) -> Any:
    return to_jsonable(
        api_upload_receipt(
            require_session(session_path),
            file_path,
            filename=filename,
            content_type=content_type,
        )
    )


def delete_receipt(receipt_id: str, *, session_path: str | None = None) -> Any:
    return to_jsonable(api_delete_receipt(require_session(session_path), receipt_id))


def match_receipt(
    receipt_id: str,
    transaction_id: str,
    *,
    session_path: str | None = None,
) -> Any:
    return to_jsonable(
        api_match_receipt(require_session(session_path), receipt_id, transaction_id)
    )


def unmatch_receipt(receipt_id: str, *, session_path: str | None = None) -> Any:
    return to_jsonable(api_unmatch_receipt(require_session(session_path), receipt_id))


def update_receipt(
    receipt_id: str,
    *,
    merchant_name: str | None = None,
    date: str | None = None,
    total_before_tax: float | None = None,
    tax: float | None = None,
    tip: float | None = None,
    grand_total: float | None = None,
    line_items: list[dict[str, Any]] | None = None,
    transaction_date: str | None = None,
    transaction_total: float | None = None,
    session_path: str | None = None,
) -> Any:
    return to_jsonable(
        api_update_receipt(
            require_session(session_path),
            receipt_id,
            merchant_name=merchant_name,
            date=date,
            total_before_tax=total_before_tax,
            tax=tax,
            tip=tip,
            grand_total=grand_total,
            line_items=receipt_line_items(line_items),
            transaction_date=transaction_date,
            transaction_total=transaction_total,
        )
    )


def get_receipt_settings(*, session_path: str | None = None) -> Any:
    return to_jsonable(api_get_receipt_settings(require_session(session_path)))


def update_receipt_settings(
    *,
    auto_categorize: bool | None = None,
    update_transaction_notes: bool | None = None,
    session_path: str | None = None,
) -> Any:
    return to_jsonable(
        api_update_receipt_settings(
            require_session(session_path),
            auto_categorize=auto_categorize,
            update_transaction_notes=update_transaction_notes,
        )
    )


def register(mcp: FastMCP) -> None:
    mcp.tool(name="receipts_list_receipts")(list_receipts)
    mcp.tool(name="receipts_get_receipt")(get_receipt)
    mcp.tool(name="receipts_upload_receipt")(upload_receipt)
    mcp.tool(name="receipts_delete_receipt")(delete_receipt)
    mcp.tool(name="receipts_match_receipt")(match_receipt)
    mcp.tool(name="receipts_unmatch_receipt")(unmatch_receipt)
    mcp.tool(name="receipts_update_receipt")(update_receipt)
    mcp.tool(name="receipts_get_receipt_settings")(get_receipt_settings)
    mcp.tool(name="receipts_update_receipt_settings")(update_receipt_settings)
