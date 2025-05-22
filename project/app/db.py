# project/app/db.py


import logging
import os
from urllib.parse import urlparse, urlunparse

from fastapi import FastAPI
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise

log = logging.getLogger("uvicorn")


def get_db_url() -> str:
    db_url = os.environ.get("DATABASE_URL", "")
    if not db_url:
        return db_url

    # Parse the URL
    parsed = urlparse(db_url)
    # Convert postgresql:// to postgres://
    if parsed.scheme == "postgresql":
        parsed = parsed._replace(scheme="postgres")
    return urlunparse(parsed)


TORTOISE_ORM = {
    "connections": {"default": get_db_url()},
    "apps": {
        "models": {
            "models": ["app.models.tortoise", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=get_db_url(),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )


async def generate_schema() -> None:
    log.info("Initializing Tortoise...")

    await Tortoise.init(
        db_url=get_db_url(),
        modules={"models": ["models.tortoise"]},
    )
    log.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(generate_schema())
