"""Network scanning utilities and Flask data-ingestion blueprint."""

from __future__ import annotations

import logging
import socket

from flask import Blueprint, jsonify, request

logger = logging.getLogger(__name__)

data_processing = Blueprint("data_processing", __name__)


# ── Flask blueprint ────────────────────────────────────────────────────────────


@data_processing.route("/data", methods=["POST"])
def receive_data():
    """Accept and validate a JSON data payload."""
    try:
        data = request.get_json()
        if not data or "input" not in data:
            logger.warning("Invalid input received")
            return jsonify({"error": "Invalid input"}), 400
        logger.info("Data processed successfully")
        return jsonify({"message": "Data received successfully"}), 200
    except Exception as exc:
        logger.error("Error processing request: %s", exc)
        return jsonify({"error": "Internal Server Error"}), 500


# ── Network helpers ────────────────────────────────────────────────────────────


def is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    """Return *True* if *port* is reachable on *host* within *timeout* seconds."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        return sock.connect_ex((host, port)) == 0


def scan_common_ports(host: str = "127.0.0.1") -> dict[int, bool]:
    """Scan a set of commonly exploited ports on *host*."""
    ports = {
        135: "RPC",
        139: "NetBIOS",
        445: "SMB",
        3389: "RDP",
    }
    results: dict[int, bool] = {}
    for port in ports:
        results[port] = is_port_open(host, port)
    return results
