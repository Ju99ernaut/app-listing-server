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
)


@router.get("/users", response_model=List[User])
async def get_all_users():
    return [user for user in data.admin_get_users()]


@router.get("/user/{id}", response_model=User)
async def get_user(id: int):
    user = data.admin_get_user(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return user


@router.delete("/user/{id}")
async def remove_user(id: int):
    data.admin_remove_user(id)


@router.delete("/application/{id}")
async def remove_application(id: int):
    data.admin_remove_application(id)


@router.delete("/rating/{id}")
async def remove_rating(id: int):
    data.admin_remove_rating(id)