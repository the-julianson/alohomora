# project/app/db.py


import logging

from fastapi import FastAPI, Request
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import get_db_url
from .orm import metadata


log = logging.getLogger("uvicorn")


def init_db(app: FastAPI) -> None:
    db_url = get_db_url()
    log.info(f"Creating engine with URL: {db_url}")
    engine = create_engine(db_url)
    metadata.create_all(engine)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Add session to app state
    app.state.db_session = session_local


def get_db_session(request: Request) -> Session:
    session_maker = request.app.state.db_session
    session = session_maker()
    try:
        yield session
    finally:
        session.close()
