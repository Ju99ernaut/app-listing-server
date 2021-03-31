import data
from datetime import timedelta

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .models import Token, TokenData, User, UserInDB, Application, Rating
from .dependencies import get_current_user
from utils.password import authenticate, create_access_token, get_hash

from constants import *

router = APIRouter(tags=["users"], responses={404: {"description": "Not found"}})


@router.post("/register", response_model=User)
async def register_user(user: UserInDB):
    data.add_user(user.username, user.email, get_hash(user.password))
    return_user = data.get_user(user.username)
    if not return_user:
        raise HTTPException(
            status_code=404, detail="Item not found, failed to register"
        )
    return return_user


@router.post("/auth", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user[USERNAME_KEY]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.delete("/users/me/")
async def unregister_users_me(current_user: User = Depends(get_current_user)):
    data.remove_user(
        current_user[USERNAME_KEY], current_user[EMAIL_KEY], current_user[PASSWORD_KEY]
    )


@router.get("/users/me/apps", response_model=List[Application])
async def read_own_apps(current_user: User = Depends(get_current_user)):
    return [apps for apps in data.get_user_applications(current_user[USERNAME_KEY])]


@router.post("/users/me/apps", response_model=Application)
async def add_app(app: Application, current_user: User = Depends(get_current_user)):
    data.add_application(
        app.image,
        app.title,
        app.by,
        app.groups,
        app.description,
        current_user[USERNAME_KEY],
    )
    return_app = data.get_application(app.title)
    if not return_app:
        raise HTTPException(status_code=404, detail="Item not found, failed to add")
    return return_app


@router.delete("/users/me/apps/{title}")
async def delete_app(title: str, current_user: User = Depends(get_current_user)):
    data.remove_application(title, current_user[USERNAME_KEY])


@router.get("/users/me/ratings", response_model=List[Rating])
async def read_own_ratings(current_user: User = Depends(get_current_user)):
    return [ratings for ratings in data.get_user_ratings(current_user[USERNAME_KEY])]


@router.get("/users/me/ratings/{application}", response_model=Rating)
async def read_own_application_rating(
    application: str, current_user: User = Depends(get_current_user)
):
    rating = data.get_user_application_ratings(current_user[USERNAME_KEY], application)
    if not rating:
        raise HTTPException(status_code=404, detail="Item not found")
    return rating


@router.post("/users/me/ratings/{application}", response_model=Rating)
async def add_app(
    application: str, rating: Rating, current_user: User = Depends(get_current_user)
):
    data.add_rating(
        current_user[USERNAME_KEY],
        application,
        rating.rating,
        rating.comment,
    )
    return_rating = data.get_user_application_ratings(
        current_user[USERNAME_KEY], application
    )
    if not return_rating:
        raise HTTPException(status_code=404, detail="Item not found, failed to add")
    return return_rating