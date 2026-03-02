# Deployment Guide

## Docker (recommended)

```bash
# Build image
docker build -t security-app .

# Run with environment variables
docker run -d \
  -p 5000:5000 \
  -e SECRET_KEY=<your-secret> \
  -e API_KEY=<your-api-key> \
  security-app
```

Or use Docker Compose:

```bash
cp .env.example .env   # fill in values
docker compose up -d
```

## Manual (Linux / macOS)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export APP_ENV=production
export SECRET_KEY=<your-secret>
gunicorn --factory "security_app.app:create_app" -b 0.0.0.0:5000
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ENV` | `development` | `development` / `production` / `testing` |
| `SECRET_KEY` | `change-me-in-production` | Flask secret key |
| `API_KEY` | *(none)* | API authentication key |
| `LOG_LEVEL` | `INFO` | Python logging level |
| `DATABASE_URL` | `sqlite:///security_app.db` | Database connection string |
| `REPORTS_DIR` | `./reports` | Directory for scan report files |

## Production Checklist

- [ ] Set a strong random `SECRET_KEY`
- [ ] Set `API_KEY`
- [ ] Set `APP_ENV=production`
- [ ] Run behind a reverse proxy (nginx / Caddy)
- [ ] Enable HTTPS
- [ ] Rotate credentials regularly
