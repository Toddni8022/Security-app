"""Main Flask application factory."""

from __future__ import annotations

import logging

from flask import Flask, jsonify, request

from security_app.config import get_config

logger = logging.getLogger(__name__)


def create_app(env: str | None = None) -> Flask:
    """Create and configure the Flask application."""
    cfg = get_config(env)

    app = Flask(__name__)
    app.config.from_object(cfg)

    logging.basicConfig(level=cfg.LOG_LEVEL)

    # ── blueprints ─────────────────────────────────────────────────────────────
    from security_app.auth.authenticator import user_auth  # noqa: PLC0415
    from security_app.scanner.network import data_processing  # noqa: PLC0415

    app.register_blueprint(user_auth)
    app.register_blueprint(data_processing)

    # ── health check ───────────────────────────────────────────────────────────
    @app.route("/health")
    def health() -> tuple:
        return jsonify({"status": "ok"}), 200

    return app


if __name__ == "__main__":  # pragma: no cover
    application = create_app()
    application.run(debug=application.config.get("DEBUG", False))
