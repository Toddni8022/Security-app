# Security App

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![CI](https://github.com/Toddni8022/Security-app/actions/workflows/ci.yml/badge.svg)

A **Windows security scanner and remediation toolkit** with a Flask REST API, automated hardening scripts, and a modular Python package structure.

---

## Security Features

- 🔍 **Port scanning** — detects open SMB (445), RPC (135), NetBIOS (139), RDP (3389)
- 🛡️ **Automated remediation** — interactive hardening script for Windows
- 🔐 **Flask API** — login, data ingestion, and health endpoints
- 📊 **Security scoring** — 0–100 risk score based on findings
- 📋 **Audit logging** — JSON remediation logs with full action history

## Architecture Overview

```
src/security_app/
├── app.py              # Flask application factory
├── config.py           # Environment-based configuration
├── models.py           # Dataclass models
├── database.py         # JSON report store
├── utils.py            # Shared utilities
├── auth/
│   ├── authenticator.py   # Login blueprint
│   └── permissions.py     # Command authorisation
└── scanner/
    ├── vulnerability.py   # Vulnerability assessment
    └── network.py         # Port scanner + data blueprint
```

## Prerequisites

- Python 3.11+
- pip
- (Optional) Docker & Docker Compose

## Installation

```bash
git clone https://github.com/Toddni8022/Security-app.git
cd Security-app
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
cp .env.example .env        # edit as needed
```

## Quick Start

```bash
# Run the Flask API
make run

# Run tests
make test

# Lint
make lint

# Security scan (bandit)
make scan
```

## Configuration

Copy `.env.example` to `.env` and set:

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Flask secret key (required in production) |
| `API_KEY` | API authentication key |
| `APP_ENV` | `development` / `production` / `testing` |
| `LOG_LEVEL` | `DEBUG` / `INFO` / `WARNING` |

## Usage

### Flask API

```bash
python -m security_app.app
```

```bash
curl -X POST http://localhost:5000/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"secret"}'

curl http://localhost:5000/health
```

### Remediation Script (Windows — requires Administrator)

```
Right-click terminal → "Run as administrator"
python remediate.py
```

### Docker

```bash
docker compose up --build
```

## Security Considerations

- Never commit `.env` files — use `.env.example` as a template
- Rotate `SECRET_KEY` and `API_KEY` regularly
- Run the Flask API behind a reverse proxy with HTTPS in production
- `remediate.py` requires Windows Administrator privileges
- See [SECURITY.md](SECURITY.md) for vulnerability reporting

## API Documentation

See [docs/api.md](docs/api.md) for full endpoint reference.

## Project Structure

```
Security-app/
├── src/security_app/   # Main Python package
├── tests/              # pytest test suite
├── docs/               # Documentation
├── remediate.py        # Windows hardening CLI
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── Makefile
└── README.md
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) © Toddni8022

