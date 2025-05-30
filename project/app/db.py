# project/app/db.py


import logging

from fastapi import FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .config import get_db_url
from .orm import metadata


log = logging.getLogger("uvicorn")


async def init_db(app: FastAPI) -> None:
    db_url = get_db_url()
    log.info(f"Creating async engine with URL: {db_url}")
    engine = create_async_engine(db_url)

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    # metadata.create_all(engine)
    async_db_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    # Add session to app state
    app.state.async_db_session = async_db_session


async def get_async_db_session(request: Request) -> AsyncSession:
    session_maker = request.app.state.async_db_session
    session = session_maker()
    try:
        yield session
    finally:
        session.close()
