# project/tests/conftest.py


import asyncio
import logging
import os
import time
import uuid

import pytest
import pytest_asyncio
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import clear_mappers
from starlette.testclient import TestClient

from app import config
from app.config import Settings, get_settings
from app.main import create_application
from app.models import Borrower
from app.orm import metadata, start_mappers


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Regular fixtures (non-async)
def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


@pytest_asyncio.fixture(scope="module")
async def app():
    app = create_application()
    app.dependency_overrides[get_settings] = lambda: Settings(
        testing=1, database_url=os.environ["DATABASE_TEST_URL"]
    )
    return app


# Async fixtures
@pytest_asyncio.fixture(scope="module")
async def async_client(app):
    await app.router.startup()
    transport = ASGITransport(app=app)
    async with AsyncClient(base_url="http://test", transport=transport) as ac:
        yield ac

    await app.router.shutdown()


@pytest_asyncio.fixture
async def in_memory_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session(in_memory_db):
    start_mappers()
    async_session_maker = async_sessionmaker(
        in_memory_db, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_maker() as session:
        yield session
    clear_mappers()


@pytest.fixture(scope="session")
def event_loop():
    """Create a single shared asyncio event loop for all async tests and fixtures.."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_test_db():
    url = config.get_db_url()
    engine = create_async_engine(url)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def postgres_db():
    engine = create_async_engine(config.get_db_url())
    await wait_for_postgres_to_come_up(engine)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def clear_database(postgres_db):
    """Clear all tables before each test."""
    async with postgres_db.begin() as conn:
        await conn.execute(
            text("""TRUNCATE TABLE
            borrowers, loans, investors, investments CASCADE""")
        )
        await conn.commit()


@pytest_asyncio.fixture
async def postgres_session(postgres_db):
    start_mappers()
    async_session_maker = async_sessionmaker(
        postgres_db, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_maker() as session:
        yield session
    clear_mappers()


@pytest_asyncio.fixture
async def add_borrower(postgres_session):
    async def __add_borrower(name, email, credit_score):
        borrower_id = str(uuid.uuid4())
        await postgres_session.execute(
            text(
                """INSERT INTO borrowers (id, name, email, credit_score)
                VALUES (:id, :name, :email, :credit_score)
                """
            ),
            {
                "id": borrower_id,
                "name": name,
                "email": email,
                "credit_score": credit_score,
            },
        )
        await postgres_session.commit()
        return Borrower(
            id=borrower_id, name=name, email=email, credit_score=credit_score
        )

    yield __add_borrower


# Helper functions
async def wait_for_webapp_to_come_up():
    deadline = time.time() + 10
    url = config.get_api_url()
    while time.time() < deadline:
        try:
            return await AsyncClient().get(url)
        except ConnectionError:
            await asyncio.sleep(0.5)
    pytest.fail("API never came up")


async def wait_for_postgres_to_come_up(engine):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
                return
        except OperationalError:
            await asyncio.sleep(0.5)
    pytest.fail("Postgres never came up")


@pytest.fixture(scope="module")
def client():
    # build exactly the same way you do in production
    app = create_application()
    # override your settings to point at web_test
    app.dependency_overrides[get_settings] = lambda: Settings(
        testing=1,
        database_url=os.environ["DATABASE_TEST_URL"],
    )
    with TestClient(app) as tc:
        yield tc
