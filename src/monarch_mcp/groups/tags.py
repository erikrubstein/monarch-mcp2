from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP
from monarch_api import (
    create_tag as api_create_tag,
    delete_tag as api_delete_tag,
    get_tag as api_get_tag,
    list_tags as api_list_tags,
    reorder_tag as api_reorder_tag,
    update_tag as api_update_tag,
)

from monarch_mcp.serialization import to_jsonable
from monarch_mcp.session import require_session


def list_tags(
    *,
    search: str | None = None,
    limit: int | None = None,
    include_transaction_count: bool = False,
    session_path: str | None = None,
) -> Any:
    return to_jsonable(
        api_list_tags(
            require_session(session_path),
            search=search,
            limit=limit,
            include_transaction_count=include_transaction_count,
        )
    )


def get_tag(tag_id: str, *, session_path: str | None = None) -> Any:
    return to_jsonable(api_get_tag(require_session(session_path), tag_id))


def create_tag(
    *,
    name: str,
    color: str,
    session_path: str | None = None,
) -> Any:
    return to_jsonable(
        api_create_tag(
            require_session(session_path),
            name=name,
            color=color,
        )
    )


def update_tag(
    tag_id: str,
    *,
    name: str | None = None,
    color: str | None = None,
    session_path: str | None = None,
) -> Any:
    return to_jsonable(
        api_update_tag(
            require_session(session_path),
            tag_id,
            name=name,
            color=color,
        )
    )


def delete_tag(tag_id: str, *, session_path: str | None = None) -> Any:
    return to_jsonable(api_delete_tag(require_session(session_path), tag_id))


def reorder_tag(
    tag_id: str,
    *,
    order: int,
    session_path: str | None = None,
) -> Any:
    return to_jsonable(
        api_reorder_tag(
            require_session(session_path),
            tag_id,
            order=order,
        )
    )


def register(mcp: FastMCP) -> None:
    mcp.tool(name="tags_list_tags")(list_tags)
    mcp.tool(name="tags_get_tag")(get_tag)
    mcp.tool(name="tags_create_tag")(create_tag)
    mcp.tool(name="tags_update_tag")(update_tag)
    mcp.tool(name="tags_delete_tag")(delete_tag)
    mcp.tool(name="tags_reorder_tag")(reorder_tag)
