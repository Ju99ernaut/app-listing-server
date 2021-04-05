from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Application(BaseModel):
    id: Optional[int] = None
    image: str
    title: str
    by: str
    groups: str
    description: str
    updated: Optional[datetime] = None
    owner: Optional[str] = None


class UpdateApplication(BaseModel):
    image: Optional[str] = None
    title: Optional[str] = None
    by: Optional[str] = None
    groups: Optional[str] = None
    description: Optional[str] = None


class Rating(BaseModel):
    id: Optional[int] = None
    user: str
    application: str
    rating: float
    comment: Optional[str] = None
    updated: Optional[datetime] = None


class RatingAverage(BaseModel):
    application: str
    rating: float


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: Optional[str] = None
    joined: Optional[datetime] = None
    admin: bool


class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None


class UserInDB(User):
    password: str