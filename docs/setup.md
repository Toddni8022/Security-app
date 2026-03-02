# Setup Guide

## Prerequisites

- Python 3.11+
- pip
- (Optional) Docker & Docker Compose

## Local Installation

```bash
# Clone the repository
git clone https://github.com/Toddni8022/Security-app.git
cd Security-app

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and edit the environment file
cp .env.example .env
```

## Running the Application

```bash
# Start the Flask API
make run
# — or —
python -m security_app.app
```

## Running Tests

```bash
make test
# — or —
pytest
```

## Docker

```bash
make docker-build
make docker-run
# — or —
docker compose up --build
```
