import data.users as data
from datetime import timedelta

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models import Token, TokenData, User, UserInDB, UpdateUser, RegisterUser
from dependencies import get_current_user, current_user_is_active
from utils.password import authenticate, create_access_token, get_hash

from constants import USERNAME_KEY, EMAIL_KEY, PASSWORD_KEY, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(tags=["users"], responses={404: {"description": "Not found"}})


@router.post("/register", response_model=User)
async def register_user(user: RegisterUser):
    if data.get_user(user.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with same username already exists",
        )
    if data.get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This email already has an account",
        )
    data.add_user(user.username, user.email, get_hash(user.password))
    return_user = data.get_user(user.username)
    if not return_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found, failed to register",
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
    return {"access_token": access_token, "token_type": "bearer", "expires_in": 3600}


@router.put("/users/me", response_model=User)
async def update_user_me(
    user: UpdateUser, current_user: User = Depends(current_user_is_active)
):
    if data.get_user(user.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with same username already exists",
        )
    db_user = data.get_user(current_user[USERNAME_KEY])
    data.update_user(db_user["id"], user)
    return data.get_user(user.username or current_user[USERNAME_KEY])


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.delete("/users/me")
async def unregister_users_me(current_user: User = Depends(get_current_user)):
    data.remove_user(
        current_user[USERNAME_KEY], current_user[EMAIL_KEY], current_user[PASSWORD_KEY]
    )