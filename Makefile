.PHONY: setup test lint scan run docker-build docker-run clean

setup:
	python -m venv .venv
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install -e .

test:
	pytest

lint:
	ruff check src/ tests/

scan:
	bandit -r src/ -ll

run:
	python -m security_app.app

docker-build:
	docker build -t security-app .

docker-run:
	docker run -p 5000:5000 --env-file .env security-app

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage dist build *.egg-info
