# project/app/db.py


import logging
import os
from urllib.parse import urlparse, urlunparse

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .orm import metadata


log = logging.getLogger("uvicorn")


def get_db_url() -> str:
    db_url = os.environ.get("DATABASE_URL", "")
    if not db_url:
        log.error("No DATABASE_URL found in environment")
        return db_url

    # Parse the URL
    parsed = urlparse(db_url)
    log.info(f"Database URL scheme: {parsed.scheme}")
    log.info(f"Database URL netloc: {parsed.netloc}")
    log.info(f"Database URL path: {parsed.path}")

    # Keep postgresql:// as is, SQLAlchemy knows how to handle it
    return urlunparse(parsed)


def init_db(app: FastAPI) -> None:
    db_url = get_db_url()
    log.info(f"Creating engine with URL: {db_url}")
    engine = create_engine(db_url)
    metadata.create_all(engine)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Add session to app state
    app.state.db_session = session_local


def generate_schema() -> None:
    log.info("Initializing SQLAlchemy...")
    db_url = get_db_url()
    log.info(f"Creating engine with URL: {db_url}")
    engine = create_engine(db_url)
    log.info("Generating database schema via SQLAlchemy...")
    metadata.create_all(engine)


if __name__ == "__main__":
    generate_schema()
