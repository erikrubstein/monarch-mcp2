from __future__ import annotations

from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP
from monarch_api import AuthSession
from monarch_api import create_session as api_create_session
from monarch_api import load_session as api_load_session
from monarch_api import save_session as api_save_session

from monarch_mcp.config import resolve_session_path
from monarch_mcp.serialization import to_jsonable
from monarch_mcp.tool_metadata import register_api_tool


REDACTED_TOKEN = "<redacted>"


def session_to_dict(
    session: AuthSession,
    *,
    include_token: bool = False,
) -> dict[str, Any]:
    data = session.to_dict()
    if not include_token:
        data["token"] = REDACTED_TOKEN
    return to_jsonable(data)  # type: ignore[return-value]


def session_from_dict(data: dict[str, Any]) -> AuthSession:
    return AuthSession.from_dict(data)


def create_session(
    email: str,
    password: str,
    *,
    mfa_code: str | None = None,
    trusted_device: bool = True,
    session_path: str | None = None,
    include_token: bool = False,
) -> dict[str, Any]:
    path = resolve_session_path(session_path) if session_path is not None else None
    session = api_create_session(
        email,
        password,
        mfa_code=mfa_code,
        trusted_device=trusted_device,
        session_path=path,
    )
    return session_to_dict(session, include_token=include_token)


def save_session(session: dict[str, Any], path: str) -> None:
    api_save_session(session_from_dict(session), Path(path).expanduser())


def load_session(path: str, *, include_token: bool = False) -> dict[str, Any]:
    session = api_load_session(Path(path).expanduser())
    return session_to_dict(session, include_token=include_token)


def register(mcp: FastMCP) -> None:
    register_api_tool(mcp, "auth", "create_session", create_session)
    register_api_tool(mcp, "auth", "save_session", save_session)
    register_api_tool(mcp, "auth", "load_session", load_session)
