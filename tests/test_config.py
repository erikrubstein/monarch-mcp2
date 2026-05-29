from __future__ import annotations

from pathlib import Path

from monarch_mcp.config import default_session_path, resolve_session_path


def test_default_session_path_uses_config_dir_env(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("MONARCH_SESSION_PATH", raising=False)
    monkeypatch.setenv("MONARCH_CONFIG_DIR", str(tmp_path))

    assert default_session_path() == tmp_path / "session.json"


def test_default_session_path_prefers_session_path_env(monkeypatch, tmp_path) -> None:
    configured = tmp_path / "custom.json"
    monkeypatch.setenv("MONARCH_SESSION_PATH", str(configured))

    assert default_session_path() == configured


def test_resolve_session_path_expands_explicit_path(tmp_path) -> None:
    explicit = tmp_path / "session.json"

    assert resolve_session_path(explicit) == Path(explicit)
