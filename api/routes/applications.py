import data.applications as data

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from models import User, Application, ApplicationReturn
from dependencies import get_current_user, current_user_is_active

from constants import USERNAME_KEY, OWNER_KEY

router = APIRouter(
    prefix="/apps",
    tags=["applications"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[ApplicationReturn])
async def read_apps():
    return [apps for apps in data.get_all_applications()]


@router.get("/{id}", response_model=ApplicationReturn)
async def read_app(id: int):
    app = data.get_application_by_id(id)
    if not app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return app


@router.get("/user/me", response_model=List[ApplicationReturn])
async def read_own_apps(current_user: User = Depends(get_current_user)):
    return [apps for apps in data.get_user_applications(current_user["id"])]


@router.post("/user/me", response_model=ApplicationReturn)
async def add_app(
    app: Application, current_user: User = Depends(current_user_is_active)
):
    if data.get_application(app.title):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Application with same title already exists",
        )
    if app.title and app.description:
        image = app.image or "default.png"
        by = app.by or current_user[USERNAME_KEY]
        groups = app.groups or "other"
        data.add_application(
            image,
            app.title,
            by,
            groups,
            app.description,
            current_user["id"],
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required fields"
        )
    return_app = data.get_application(app.title)
    if not return_app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found, failed to add",
        )
    return return_app


@router.put("/user/me/{id}", response_model=ApplicationReturn)
async def update_application(
    id: int,
    app: Application,
    current_user: User = Depends(current_user_is_active),
):
    if data.get_application(app.title):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Application with same title already exists",
        )
    db_app = data.get_application_by_id(id)
    if db_app[OWNER_KEY] != current_user[USERNAME_KEY]:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Not allowed"
        )
    data.update_application(db_app["id"], app)
    return data.get_application(app.title or title)


@router.delete("/user/me/{id}")
async def delete_app(id: int, current_user: User = Depends(current_user_is_active)):
    data.remove_application(id, current_user["id"])