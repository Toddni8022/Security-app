"""User authentication Flask blueprint."""

from __future__ import annotations

import logging
import os

from flask import Blueprint, jsonify, request

logger = logging.getLogger(__name__)

user_auth = Blueprint("user_auth", __name__)


@user_auth.route("/login", methods=["POST"])
def login():
    """Authenticate a user with username and password."""
    try:
        data = request.get_json()
        if not data or "username" not in data or "password" not in data:
            logger.warning("Invalid login attempt — missing credentials")
            return jsonify({"error": "Invalid input"}), 400
        # Authentication logic would go here
        logger.info("User logged in: %s", data.get("username"))
        return jsonify({"message": "Login successful"}), 200
    except Exception as exc:
        logger.error("Error logging in: %s", exc)
        return jsonify({"error": "Internal Server Error"}), 500
