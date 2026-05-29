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
    @mcp.tool(name="auth_create_session")
    def auth_create_session(
        email: str,
        password: str,
        mfa_code: str | None = None,
        trusted_device: bool = True,
        session_path: str | None = None,
        include_token: bool = False,
    ) -> dict[str, Any]:
        """Create a Monarch auth session.

        Maps to `monarch_api.create_session`. By default the returned
        AuthSession-shaped object redacts `token`; set `include_token` only when
        the caller explicitly needs the raw bearer token.

        Args:
            email: Monarch account email address.
            password: Monarch account password.
            mfa_code: Multi-factor authentication code, if required.
            trusted_device: Ask Monarch to remember this device.
            session_path: Optional path for the saved session file.
            include_token: Include the raw bearer token in the returned session.
        """
        return create_session(
            email,
            password,
            mfa_code=mfa_code,
            trusted_device=trusted_device,
            session_path=session_path,
            include_token=include_token,
        )

    @mcp.tool(name="auth_save_session")
    def auth_save_session(session: dict[str, Any], path: str) -> None:
        """Save a Monarch auth session to disk.

        Args:
            session: AuthSession-shaped object containing token,
                token_expiration, user_id, and email.
            path: Destination session file path.
        """
        return save_session(session, path)

    @mcp.tool(name="auth_load_session")
    def auth_load_session(path: str, include_token: bool = False) -> dict[str, Any]:
        """Load a Monarch auth session from disk.

        Maps to `monarch_api.load_session`. By default the returned
        AuthSession-shaped object redacts `token`; set `include_token` only when
        the caller explicitly needs the raw bearer token.

        Args:
            path: Session file path.
            include_token: Include the raw bearer token in the returned session.
        """
        return load_session(path, include_token=include_token)
