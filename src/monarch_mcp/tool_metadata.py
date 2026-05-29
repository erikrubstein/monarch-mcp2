from __future__ import annotations

from collections.abc import Callable

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations


READ_PREFIXES = ("download_", "get_", "list_", "load_", "search_")
WRITE_PREFIXES = (
    "archive_",
    "clear_",
    "contribute_",
    "create_",
    "link_",
    "match_",
    "reactivate_",
    "reorder_",
    "reset_",
    "restore_",
    "save_",
    "set_",
    "unmatch_",
    "unlink_",
    "unsplit_",
    "update_",
    "upload_",
    "withdraw_",
)
DESTRUCTIVE_PREFIXES = ("clear_", "delete_", "remove_", "reset_")


def register_api_tool(
    mcp: FastMCP,
    group: str,
    function_name: str,
    function: Callable,
) -> None:
    tool_name = f"{group}_{function_name}"
    mcp.tool(
        name=tool_name,
        title=_title(group, function_name),
        description=_description(function_name),
        annotations=_annotations(function_name),
    )(function)


def _description(function_name: str) -> str:
    action = function_name.replace("_", " ")
    description = f"{action.capitalize()} via monarch_api.{function_name}."
    if function_name.startswith(DESTRUCTIVE_PREFIXES):
        description += " This may delete, clear, reset, or otherwise remove data."
    elif function_name.startswith(WRITE_PREFIXES):
        description += " This may create or update Monarch data."
    return description


def _annotations(function_name: str) -> ToolAnnotations:
    read_only = function_name.startswith(READ_PREFIXES)
    destructive = function_name.startswith(DESTRUCTIVE_PREFIXES)
    return ToolAnnotations(
        title=_title("", function_name).strip(),
        readOnlyHint=read_only,
        destructiveHint=destructive,
        idempotentHint=read_only,
        openWorldHint=True,
    )


def _title(group: str, function_name: str) -> str:
    words = [
        word.capitalize()
        for word in f"{group} {function_name}".replace("_", " ").split()
    ]
    return " ".join(word for word in words if word)
