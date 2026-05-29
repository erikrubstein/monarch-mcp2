from __future__ import annotations

from monarch_api import AuthSession

from monarch_mcp.groups import auth


def test_create_session_maps_to_api_and_redacts_token(monkeypatch, tmp_path) -> None:
    def fake_create_session(*args, **kwargs) -> AuthSession:
        return AuthSession(
            token="token-123",
            token_expiration="2030-01-01T00:00:00Z",
            user_id="user-123",
            email="person@example.com",
        )

    monkeypatch.setattr(auth, "api_create_session", fake_create_session)

    result = auth.create_session(
        "person@example.com",
        "secret",
        mfa_code="123456",
        session_path=str(tmp_path / "session.json"),
    )

    assert result == {
        "token": "<redacted>",
        "token_expiration": "2030-01-01T00:00:00Z",
        "user_id": "user-123",
        "email": "person@example.com",
    }


def test_create_session_can_return_token_when_explicit(monkeypatch) -> None:
    def fake_create_session(*args, **kwargs) -> AuthSession:
        return AuthSession(
            token="token-123",
            token_expiration="2030-01-01T00:00:00Z",
            user_id="user-123",
            email="person@example.com",
        )

    monkeypatch.setattr(auth, "api_create_session", fake_create_session)

    result = auth.create_session(
        "person@example.com",
        "secret",
        include_token=True,
    )

    assert result["token"] == "token-123"
    assert result["email"] == "person@example.com"


def test_save_and_load_session_map_to_api(tmp_path) -> None:
    session_path = tmp_path / "session.json"
    session = {
        "token": "token-123",
        "token_expiration": "2030-01-01T00:00:00Z",
        "user_id": "user-123",
        "email": "person@example.com",
    }

    auth.save_session(session, str(session_path))
    redacted = auth.load_session(str(session_path))
    unredacted = auth.load_session(str(session_path), include_token=True)

    assert redacted == {
        "token": "<redacted>",
        "token_expiration": "2030-01-01T00:00:00Z",
        "user_id": "user-123",
        "email": "person@example.com",
    }
    assert unredacted["token"] == "token-123"
