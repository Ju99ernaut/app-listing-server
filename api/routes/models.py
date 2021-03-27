from typing import Optional, List
from pydantic import BaseModel


class Application(BaseModel):
    image: str
    title: str
    by: str
    groups: List(str)


class Rating(BaseModel):
    user: str
    application: str
    rating: float


class RatingAverage(BaseModel):
    application: str
    rating: float


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    password: str