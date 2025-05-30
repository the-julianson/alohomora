# project/app/config.py
import logging
import os
from functools import lru_cache
from urllib.parse import urlparse, urlunparse

from pydantic import AnyUrl
from pydantic_settings import BaseSettings


log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = 0
    database_url: AnyUrl = None


@lru_cache
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 8000 if host == "localhost" else 80
    return f"http://{host}:{port}"


def sanitize_db_url(db_url: str) -> str:
    sanitized_db_url = db_url
    if sanitized_db_url.startswith("postgres://"):
        sanitized_db_url = sanitized_db_url.replace(
            "postgres://", "postgresql+asyncpg://", 1
        )
    return sanitized_db_url


def get_db_url() -> str:
    db_url = os.environ.get("DATABASE_URL", "")
    if not db_url:
        log.error("No DATABASE_URL found in environment")
        return db_url

    db_url = sanitize_db_url(db_url)

    # Parse the URL
    parsed = urlparse(db_url)
    log.info(f"Database URL scheme: {parsed.scheme}")
    log.info(f"Database URL netloc: {parsed.netloc}")
    log.info(f"Database URL path: {parsed.path}")

    # Keep postgresql:// as is, SQLAlchemy knows how to handle it
    return urlunparse(parsed)
