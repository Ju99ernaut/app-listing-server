import data

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from .models import Application

router = APIRouter(
    prefix="/apps", tags=["applications"], responses={404: {"description": "Not found"}}
)


@router.get("", response_model=List[Application])
async def read_apps():
    return [apps for apps in data.get_all_applications()]


@router.get("/{title}", response_model=Application)
async def read_app(title: str):
    app = data.get_application(title)
    if not app:
        raise HTTPException(status_code=404, detail="Item not found")
    return app