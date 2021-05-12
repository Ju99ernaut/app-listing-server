import data.meta as data

from fastapi import APIRouter, Path
from models import Count

router = APIRouter(prefix="/meta", tags=["meta"])


@router.get("/users", response_model=Count)
async def get_users_count():
    return {"count": data.get_users_count()}


@router.get("/apps", response_model=Count)
async def get_apps_count():
    return {"count": data.get_apps_count()}


@router.get("/ratings/{application}", response_model=Count)
async def get_app_ratings_count(
    application: int = Path(..., description="Application ID")
):
    return {"count": data.get_app_ratings_count(application)}
