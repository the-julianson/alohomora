from fastapi import APIRouter, Depends

from app.config import Settings, get_settings


router = APIRouter(prefix="/v1")


@router.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    """
    Health check endpoint that returns basic system information.
    This endpoint should be lightweight and fast.
    """
    return {
        "status": "healthy",
        "environment": settings.environment,
        "testing": settings.testing,
        "database_url": settings.database_url,
    }


@router.get("/version")
async def version():
    """
    API version endpoint that returns version information.
    This follows semantic versioning (MAJOR.MINOR.PATCH).
    """
    return {
        "version": "1.0.0",
        "name": "Alohomora Loan Management System",
        "api_version": "v1",
        "semantic_version": {
            "major": 1,
            "minor": 0,
            "patch": 0
        }
    }
