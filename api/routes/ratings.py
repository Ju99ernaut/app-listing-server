import data.ratings as data
import data.applications as apps_data

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from models import User, Rating, RatingAverage, RatingReturn, Message
from dependencies import get_current_user, current_user_is_active

router = APIRouter(
    prefix="/ratings",
    tags=["ratings"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[RatingReturn])
async def read_ratings(
    page: Optional[int] = Query(0, minimum=0, description="Page number"),
    size: Optional[int] = Query(50, maximum=100, description="Page size"),
):
    return [ratings for ratings in data.get_all_ratings()]


@router.get("/user/{user}", response_model=List[RatingReturn])
async def read_user_ratings(
    user: int = Path(..., description="User ID"),
    page: Optional[int] = Query(0, minimum=0, description="Page number"),
    size: Optional[int] = Query(50, maximum=100, description="Page size"),
):
    return [ratings for ratings in data.get_user_ratings(user)]


@router.get("/app/{application}", response_model=List[RatingReturn])
async def read_app_ratings(
    application: int = Path(..., description="Application ID"),
    page: Optional[int] = Query(0, minimum=0, description="Page number"),
    size: Optional[int] = Query(50, maximum=100, description="Page size"),
):
    return [ratings for ratings in data.get_application_ratings(application)]


@router.get("/average/{application}", response_model=RatingAverage)
async def read_app_average(application: int = Path(..., description="Application ID")):
    rating = data.get_average_rating(application)
    application_dict = apps_data.get_application_by_id(application)
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return {"application": application_dict, "rating": rating}


@router.get("/averages", response_model=List[RatingAverage])
async def read_all_app_averages(
    page: Optional[int] = Query(0, minimum=0, description="Page number"),
    size: Optional[int] = Query(50, maximum=100, description="Page size"),
):
    return data.get_all_average_ratings()


@router.get("/me", response_model=List[RatingReturn])
async def read_own_ratings(
    current_user: User = Depends(get_current_user),
    page: Optional[int] = Query(0, minimum=0, description="Page number"),
    size: Optional[int] = Query(50, maximum=100, description="Page size"),
):
    return [ratings for ratings in data.get_user_ratings(current_user["id"])]


@router.get("/me/{application}", response_model=RatingReturn)
async def read_own_application_rating(
    application: int = Path(..., description="Application ID"),
    current_user: User = Depends(get_current_user),
):
    rating = data.get_user_application_ratings(current_user["id"], application)
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return rating


@router.post("/{application}", response_model=RatingReturn)
async def add_update_application_rating(
    rating: Rating,
    application: int = Path(..., description="Application ID"),
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


@router.delete("/{rating}", response_model=Message)
async def delete_app_rating(
    rating: int = Path(..., description="Rating ID"),
    current_user: User = Depends(current_user_is_active),
):
    data.remove_rating(rating, current_user["id"])
    if data.get_rating_by_id(rating):
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Failed to delete"
        )
    return {"msg": "deleted"}