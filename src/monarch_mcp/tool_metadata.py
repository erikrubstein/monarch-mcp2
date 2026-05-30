from __future__ import annotations

import inspect
from collections.abc import Callable
from functools import wraps
from typing import Annotated, Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from monarch_mcp.output import OutputMode, shape_output
from monarch_mcp.serialization import raw_output


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
    wrapped = _with_output_controls(tool_name, function)
    mcp.tool(
        name=tool_name,
        title=_title(group, function_name),
        description=_description(function_name),
        annotations=_annotations(function_name),
    )(wrapped)


def _with_output_controls(tool_name: str, function: Callable) -> Callable:
    @wraps(function)
    def wrapped(
        *args: Any,
        output_mode: OutputMode = "summary",
        fields: list[str] | None = None,
        **kwargs: Any,
    ) -> Any:
        with raw_output(output_mode == "raw"):
            result = function(*args, **kwargs)
        return shape_output(tool_name, result, output_mode=output_mode, fields=fields)

    wrapped.__signature__ = _signature_with_output_controls(function)  # type: ignore[attr-defined]
    wrapped.__annotations__ = {
        "output_mode": OutputMode,
        "fields": list[str] | None,
        "return": Any,
    }
    return wrapped


def _signature_with_output_controls(function: Callable) -> inspect.Signature:
    signature = inspect.signature(function, eval_str=True)
    parameters = list(signature.parameters.values())
    parameters.extend(
        [
            inspect.Parameter(
                "output_mode",
                inspect.Parameter.KEYWORD_ONLY,
                default="summary",
                annotation=Annotated[
                    OutputMode,
                    Field(
                        description=(
                            "Output shape to return. Use summary for compact CLI-style "
                            "defaults, full for complete structured data without raw, "
                            "and raw for complete structured data including raw payloads."
                        )
                    ),
                ],
            ),
            inspect.Parameter(
                "fields",
                inspect.Parameter.KEYWORD_ONLY,
                default=None,
                annotation=Annotated[
                    list[str] | None,
                    Field(
                        description=(
                            "Optional dotted output field paths to return, such as "
                            "['id', 'merchant.name', 'category.name']."
                        )
                    ),
                ],
            ),
        ]
    )
    return signature.replace(parameters=parameters, return_annotation=Any)


def _description(function_name: str) -> str:
    action = function_name.replace("_", " ")
    description = f"{action.capitalize()}."
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
