# Architecture

## Overview

```
Security-app/
├── src/security_app/          # Main Python package
│   ├── app.py                 # Flask application factory
│   ├── config.py              # Environment-based configuration
│   ├── models.py              # Dataclass models (Finding, ScanReport, …)
│   ├── database.py            # JSON-backed report & log store
│   ├── utils.py               # Shared utilities
│   ├── auth/
│   │   ├── authenticator.py   # Login Flask blueprint
│   │   └── permissions.py     # Discord command authorisation
│   └── scanner/
│       ├── vulnerability.py   # Vulnerability assessment helpers
│       └── network.py         # Port scanning + data-ingestion blueprint
├── tests/                     # pytest test suite
├── docs/                      # Project documentation
├── remediate.py               # Windows remediation CLI (standalone)
├── Dockerfile / docker-compose.yml
└── pyproject.toml
```

## Component Interaction

```
Client
  │
  ▼
Flask API (app.py)
  ├── /login  ──►  auth/authenticator.py
  ├── /data   ──►  scanner/network.py
  └── /health ──►  (inline)

CLI Tools
  ├── remediate.py  ──►  scanner/vulnerability.py
  └── daily_check.py ──► database.py (ReportStore)
```

## Configuration

All configuration is read from environment variables via `config.py`.  
No secrets are hard-coded; see `.env.example` for a full list.

## Data Flow

1. Scans run and produce `Finding` objects.
2. Findings are aggregated into a `ScanReport` and persisted by `ReportStore`.
3. `assess_score()` converts findings into a 0-100 security score.
4. Results are surfaced via the Flask API or written to JSON files.
