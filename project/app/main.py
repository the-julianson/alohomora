# project/app/main.py


import logging

from fastapi import FastAPI

from app.api import ping


logging.basicConfig(level=logging.INFO)


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router)

    return application


app = create_application()
