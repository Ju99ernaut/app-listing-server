import data

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from .models import Rating, RatingAverage

router = APIRouter(
    prefix="/ratings", tags=["ratings"], responses={404: {"description": "Not found"}}
)


@router.get("", response_model=List[Rating])
async def read_ratings():
    return [ratings for ratings in data.get_all_ratings()]


@router.get("/user/{user}", response_model=List[Rating])
async def read_user_ratings(user: str):
    return [ratings for ratings in data.get_user_ratings(user)]


@router.get("/app/{application}", response_model=List[Rating])
async def read_app_ratings(application: str):
    return [ratings for ratings in data.get_application_ratings(application)]


@router.get("/average/{application}", response_model=RatingAverage)
async def read_app_average(application: str):
    rating = data.get_average_rating(application)
    if not rating:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"application": application, "rating": rating}


@router.get("/averages", response_model=List[RatingAverage])
async def read_all_app_averages():
    return data.get_all_average_ratings()