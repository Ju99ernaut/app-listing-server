import data.applications as data

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from models import User, Application, ApplicationUpdate, ApplicationReturn, Message
from dependencies import get_current_user, current_user_is_active, current_user_can_list

from constants import USERNAME_KEY, OWNER_KEY

router = APIRouter(
    prefix="/apps",
    tags=["applications"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[ApplicationReturn])
async def read_apps(
    page: Optional[int] = Query(0, minimum=0, description="Page number"),
    size: Optional[int] = Query(50, maximum=100, description="Page size"),
):
    return data.get_all_applications(size, page)


@router.get("/me", response_model=List[ApplicationReturn])
async def read_own_apps(
    current_user: User = Depends(get_current_user),
    page: Optional[int] = Query(0, minimum=0, description="Page number"),
    size: Optional[int] = Query(50, maximum=100, description="Page size"),
):
    return data.get_user_applications(current_user["id"], size, page)


@router.get("/{application}", response_model=ApplicationReturn)
async def read_app(application: int = Path(..., description="Application ID")):
    app = data.get_application_by_id(application)
    if not app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return app


@router.post("", response_model=ApplicationReturn)
async def add_app(
    app: Application, current_user: User = Depends(current_user_can_list)
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
            app.status,
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


@router.put("/{application}", response_model=ApplicationReturn)
async def update_application(
    app: ApplicationUpdate,
    application: int = Path(..., description="Application ID"),
    current_user: User = Depends(current_user_is_active),
):
    if data.get_application(app.title):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Application with same title already exists",
        )
    db_app = data.get_application_by_id(application)
    if db_app[OWNER_KEY]["id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Not allowed"
        )
    data.update_application(db_app["id"], app)
    return data.get_application_by_id(db_app["id"])


@router.delete("/{application}", response_model=Message)
async def delete_app(
    application: int = Path(..., description="Application ID"),
    current_user: User = Depends(current_user_is_active),
):
    data.remove_application(application, current_user["id"])
    if data.get_application_by_id(application):
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Failed to delete"
        )
    return {"msg": "deleted"}