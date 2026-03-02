FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir flask==3.1.0 gunicorn==22.0.0

# Copy source
COPY src/ src/
COPY setup.py pyproject.toml ./

RUN pip install --no-cache-dir -e .

ENV APP_ENV=production
ENV LOG_LEVEL=INFO

EXPOSE 5000

CMD ["gunicorn", "--factory", "security_app.app:create_app", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "2", \
     "--timeout", "60"]
