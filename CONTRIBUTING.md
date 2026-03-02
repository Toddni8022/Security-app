# Contributing to Security-app

Thank you for your interest in contributing! Here's how to get started.

## Development Setup

```bash
git clone https://github.com/Toddni8022/Security-app.git
cd Security-app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Running Tests

```bash
make test
```

## Code Style

This project uses **ruff** for linting and formatting:

```bash
make lint
```

## Submitting a Pull Request

1. Fork the repository and create a feature branch from `main`.
2. Write tests for any new functionality.
3. Ensure `make test` and `make lint` pass.
4. Open a Pull Request with a clear description of your changes.

## Reporting Bugs

Please use GitHub Issues. For security vulnerabilities, see [SECURITY.md](SECURITY.md).

## Code of Conduct

Be respectful and constructive. Harassment of any kind will not be tolerated.
