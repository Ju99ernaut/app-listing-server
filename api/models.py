from enum import Enum
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: Optional[int] = None


class TokenData(BaseModel):
    username: Optional[str] = None


class RoleName(str, Enum):
    user = "user"
    admin = "admin"


class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    joined: Optional[datetime] = None
    active: bool
    role: RoleName


class UpdateUser(BaseModel):
    def __getitem__(self, item):
        return getattr(self, item)

    username: Optional[str] = None
    email: Optional[str] = None


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserInDB(User):
    password: str


class Application(BaseModel):
    def __getitem__(self, item):
        return getattr(self, item)

    image: Optional[str] = None
    title: str
    by: Optional[str] = None
    groups: List[str]
    description: str


class ApplicationReturn(BaseModel):
    id: Optional[int] = None
    image: Optional[str] = None
    title: str
    by: Optional[str] = None
    groups: List[str]
    description: str
    updated: Optional[datetime] = None
    owner: User


class Documentation(BaseModel):
    application: int
    documentation: str
    updated: Optional[datetime] = None


class DocumentationReturn(BaseModel):
    id: Optional[int] = None
    application: ApplicationReturn
    documentation: str
    updated: Optional[datetime] = None
    owner: User


class Rating(BaseModel):
    user: int
    application: int
    rating: float
    comment: Optional[str] = None


class RatingReturn(BaseModel):
    id: Optional[int] = None
    user: User
    application: ApplicationReturn
    rating: float
    comment: Optional[str] = None
    updated: Optional[datetime] = None


class RatingAverage(BaseModel):
    application: ApplicationReturn
    rating: Optional[float] = 0