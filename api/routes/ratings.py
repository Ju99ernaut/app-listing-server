import data.ratings as data

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from models import User, Rating, RatingAverage, RatingReturn
from dependencies import get_current_user, current_user_is_active

router = APIRouter(
    prefix="/ratings",
    tags=["ratings"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[RatingReturn])
async def read_ratings():
    return [ratings for ratings in data.get_all_ratings()]


@router.get("/users/{user}", response_model=List[RatingReturn])
async def read_user_ratings(user: int):
    return [ratings for ratings in data.get_user_ratings(user)]


@router.get("/app/{application}", response_model=List[RatingReturn])
async def read_app_ratings(application: int):
    return [ratings for ratings in data.get_application_ratings(application)]


@router.get("/average/{application}", response_model=RatingAverage)
async def read_app_average(application: int):
    rating = data.get_average_rating(application)
    application_dict = data.get_application_by_id(application)
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return {"application": application_dict, "rating": rating}


@router.get("/averages", response_model=List[RatingAverage])
async def read_all_app_averages():
    return data.get_all_average_ratings()


@router.get("/user/me", response_model=List[RatingReturn])
async def read_own_ratings(current_user: User = Depends(get_current_user)):
    return [ratings for ratings in data.get_user_ratings(current_user["id"])]


@router.get("/user/me/{application}", response_model=RatingReturn)
async def read_own_application_rating(
    application: int, current_user: User = Depends(get_current_user)
):
    rating = data.get_user_application_ratings(current_user["id"], application)
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return rating


@router.post("/user/me/{application}", response_model=RatingReturn)
async def add_application_rating(
    application: int,
    rating: Rating,
    current_user: User = Depends(current_user_is_active),
):
    if rating.rating:
        data.add_rating(
            current_user["id"],
            application,
            rating.rating,
            rating.comment,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required fields"
        )
    return_rating = data.get_user_application_ratings(current_user["id"], application)
    if not return_rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found, failed to add",
        )
    return return_rating


@router.delete("/user/me/{id}")
async def delete_app_rating(
    id: int, current_user: User = Depends(current_user_is_active)
):
    data.remove_rating(id, current_user["id"])