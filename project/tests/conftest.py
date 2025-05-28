# project/tests/conftest.py


import logging
import os
import time
import uuid
from pathlib import Path

import pytest
import requests
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import clear_mappers, sessionmaker
from starlette.testclient import TestClient

from app import config
from app.config import Settings, get_settings
from app.main import create_application
from app.models import Borrower
from app.orm import metadata, start_mappers


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_settings_override():
    return Settings(
        testing=1, database_url=os.environ.get("DATABASE_TEST_URL")
    )


@pytest.fixture(scope="module")
def test_app():
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()

def wait_for_webapp_to_come_up():
    deadline = time.time() + 10
    url = config.get_api_url()
    while time.time() < deadline:
        try:
            return requests.get(url)
        except ConnectionError:
            time.sleep(0.5)
    pytest.fail("API never came up")

def wait_for_postgres_to_come_up(engine):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            return engine.connect()
        except OperationalError:
            time.sleep(0.5)
    pytest.fail("Postgres never came up")

@pytest.fixture(scope="session")
def postgres_db():
    engine = create_engine(config.get_db_url())
    wait_for_postgres_to_come_up(engine)
    metadata.create_all(engine)
    return engine


@pytest.fixture
def postgres_session(postgres_db):
    start_mappers()
    yield sessionmaker(bind=postgres_db)()
    clear_mappers()


@pytest.fixture
def add_borrower(postgres_session):
    def __add_borrower(name, email, credit_score):
        borrower_id = str(uuid.uuid4())
        postgres_session.execute(
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
        postgres_session.commit()
        return Borrower(
            id=borrower_id,
            name=name,
            email=email,
            credit_score=credit_score
        )
    yield __add_borrower


@pytest.fixture
def restart_api():
    (Path(__file__).parent / "main.py").touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()
