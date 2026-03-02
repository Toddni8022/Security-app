# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [1.0.0] — 2026-03-02

### Added
- `src/security_app/` proper Python package structure
- `src/security_app/auth/` authentication sub-package (authenticator, permissions)
- `src/security_app/scanner/` scanning sub-package (vulnerability, network)
- `src/security_app/models.py` — dataclass models (Finding, ScanReport, etc.)
- `src/security_app/database.py` — JSON-backed ReportStore
- `src/security_app/config.py` — environment-based configuration
- `src/security_app/utils.py` — shared utility functions
- `tests/` — pytest test suite (test_app, test_auth, test_scanner, test_models)
- `docs/` — setup, architecture, API, security features, deployment guides
- `Dockerfile` and `docker-compose.yml`
- `.github/workflows/ci.yml` — CI pipeline (lint, test, security scan)
- `pyproject.toml` with full project metadata and tool configuration
- `Makefile` for common developer tasks
- `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE`

### Changed
- Updated `README.md` with badges, architecture overview, and full usage docs
- Updated `requirements.txt` with pinned versions
