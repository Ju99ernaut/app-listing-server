import data.admin as data

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from models import User
from dependencies import current_user_is_admin

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(current_user_is_admin)],
    include_in_schema=False,
)


@router.get("/users", response_model=List[User])
async def get_all_users():
    return [user for user in data.admin_get_users()]


@router.get("/user/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = data.admin_get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return user


@router.delete("/user/{user_id}")
async def remove_user(user_id: int):
    data.admin_remove_user(user_id)


@router.delete("/application/{app_id}")
async def remove_application(app_id: int):
    data.admin_remove_application(app_id)


@router.delete("/rating/{rating_id}")
async def remove_rating(rating_id: int):
    data.admin_remove_rating(rating_id)


@router.delete("/documentation/{doc_id}")
async def remove_documentation(doc_id: int):
    data.admin_remove_documentation(doc_id)