# project/app/main.py


from fastapi import FastAPI

from app.api import ping


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router)

    return application


app = create_application()
