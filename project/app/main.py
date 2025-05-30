# project/app/main.py


import logging

from fastapi import FastAPI

from app.api import loans, ping
from app.db import init_db
from app.orm import start_mappers


logging.basicConfig(level=logging.INFO)


def create_application() -> FastAPI:
    logging.info("Starting mappers...")
    start_mappers()

    logging.info("Creating FastAPI application...")
    application = FastAPI()

    logging.info("Initializing database...")

    @application.on_event("startup")
    async def on_startup():
        logging.info("Initializing async DB…")
        await init_db(application)

    application.include_router(ping.router)
    application.include_router(loans.router)

    return application


app = create_application()
