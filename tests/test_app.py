"""Tests for the Flask application routes."""

import json


def test_health_endpoint(client):
    """GET /health returns 200 and status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "ok"


def test_login_missing_fields(client):
    """POST /login without credentials returns 400."""
    response = client.post(
        "/login",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert response.status_code == 400


def test_login_success(client):
    """POST /login with valid fields returns 200."""
    payload = {"username": "admin", "password": "secret"}
    response = client.post(
        "/login",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Login successful"


def test_data_endpoint_missing_input(client):
    """POST /data without 'input' key returns 400."""
    response = client.post(
        "/data",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert response.status_code == 400


def test_data_endpoint_success(client):
    """POST /data with valid payload returns 200."""
    payload = {"input": "test data"}
    response = client.post(
        "/data",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Data received successfully"
