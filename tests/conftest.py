"""Pytest configuration and shared fixtures."""

import pytest

from security_app.app import create_app


@pytest.fixture()
def app():
    """Create an application instance configured for testing."""
    application = create_app("testing")
    application.config["TESTING"] = True
    yield application


@pytest.fixture()
def client(app):
    """Return a test client for the Flask app."""
    return app.test_client()
