import data

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from .models import User, UserInDB, Application, Rating
from .dependencies import current_user_is_admin

from constants import *

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(current_user_is_admin)],
)


@router.delete("/user/{id}")
async def remove_user(id: int):
    data.admin_remove_user(id)


@router.delete("/application/{id}")
async def remove_application(id: int):
    data.admin_remove_application(id)


@router.delete("/rating/{id}")
async def remove_rating(id: int):
    data.admin_remove_rating(id)