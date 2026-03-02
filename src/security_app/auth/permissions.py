"""Permission helpers and Discord command authorisation."""

from __future__ import annotations

import os

# Authorised Discord user ID (overridable via environment variable)
DISCORD_USER_ID: str = os.getenv("DISCORD_USER_ID", "1066217565795397682")


def is_authorised(user_id: str) -> bool:
    """Return *True* if *user_id* matches the configured authorised user."""
    return user_id == DISCORD_USER_ID


def require_authorised(user_id: str) -> str | None:
    """Return an error string if *user_id* is not authorised, else *None*."""
    if not is_authorised(user_id):
        return "Unauthorized command."
    return None
