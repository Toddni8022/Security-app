"""Tests for authentication modules."""

import pytest

from security_app.auth.permissions import is_authorised, require_authorised

AUTHORISED_ID = "1066217565795397682"
UNKNOWN_ID = "9999999999999999999"


def test_is_authorised_valid(monkeypatch):
    monkeypatch.setenv("DISCORD_USER_ID", AUTHORISED_ID)
    # Re-import to pick up new env var value
    import importlib
    import security_app.auth.permissions as perms
    importlib.reload(perms)
    assert perms.is_authorised(AUTHORISED_ID) is True


def test_is_authorised_invalid(monkeypatch):
    monkeypatch.setenv("DISCORD_USER_ID", AUTHORISED_ID)
    import importlib
    import security_app.auth.permissions as perms
    importlib.reload(perms)
    assert perms.is_authorised(UNKNOWN_ID) is False


def test_require_authorised_returns_none_for_valid():
    import importlib
    import security_app.auth.permissions as perms
    importlib.reload(perms)
    result = perms.require_authorised(perms.DISCORD_USER_ID)
    assert result is None


def test_require_authorised_returns_error_for_invalid():
    import importlib
    import security_app.auth.permissions as perms
    importlib.reload(perms)
    result = perms.require_authorised(UNKNOWN_ID)
    assert result == "Unauthorized command."
