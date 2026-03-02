"""Application configuration loaded from environment variables."""

import os


class Config:
    """Base configuration."""

    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    API_KEY: str | None = os.getenv("API_KEY")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///security_app.db")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Audit
    INACTIVITY_THRESHOLD_HOURS: int = int(
        os.getenv("INACTIVITY_THRESHOLD_HOURS", "12")
    )
    REPORTS_DIR: str = os.getenv("REPORTS_DIR", "./reports")

    # Discord
    DISCORD_USER_ID: str = os.getenv(
        "DISCORD_USER_ID", "1066217565795397682"
    )


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False


class TestingConfig(Config):
    """Testing configuration."""

    DEBUG = True
    DATABASE_URL = "sqlite:///:memory:"


_configs = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config(env: str | None = None) -> type[Config]:
    """Return the configuration class for *env* (defaults to ``APP_ENV``)."""
    env = env or os.getenv("APP_ENV", "development")
    return _configs.get(env, DevelopmentConfig)
