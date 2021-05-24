from enum import Enum
from typing import Optional, List, Union
from pydantic import BaseModel, EmailStr, AnyHttpUrl, validator
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: Optional[int] = 3600


class TokenData(BaseModel):
    username: Optional[str] = None


class RoleName(str, Enum):
    user = "user"
    developer = "developer"
    admin = "admin"


class UserRef(BaseModel):
    id: Optional[int] = 1
    username: str
    joined: Optional[datetime] = None
    active: bool


class User(UserRef):
    email: EmailStr
    role: RoleName


class UpdateUser(BaseModel):
    def __getitem__(self, item):
        return getattr(self, item)

    username: Optional[str] = None
    email: Optional[EmailStr] = None

    @validator("username")
    def no_space(cls, v):
        if " " in v:
            raise ValueError("value must not contain spaces")
        return v


class RegisterUser(UpdateUser):
    username: str
    email: EmailStr
    password: str


class UserInDB(User):
    password: str


class Application(BaseModel):
    def __getitem__(self, item):
        return getattr(self, item)

    image: Optional[str] = None
    title: str
    by: Optional[str] = None
    status: Optional[str] = ""
    groups: Union[List[str], str]
    description: str

    @validator("groups")
    def stringify(cls, v):
        if type(v) == list:
            return ",".join(v)
        return v


class ApplicationRef(BaseModel):
    id: Optional[int] = 1
    image: Optional[str] = "default.png"
    title: str
    by: Optional[str] = None
    status: Optional[str] = ""
    groups: Union[List[str], str]
    description: str
    updated: Optional[datetime] = None

    @validator("groups")
    def listify(cls, v):
        if type(v) == str:
            return v.split(",")
        return v


class ApplicationReturn(ApplicationRef):
    owner: UserRef


class Documentation(BaseModel):
    external: Optional[str] = ""
    documentation: str


class DocumentationReturn(BaseModel):
    id: Optional[int] = 1
    external: Optional[AnyHttpUrl] = ""
    documentation: str
    application: ApplicationRef
    updated: Optional[datetime] = None


class Rating(BaseModel):
    rating: float
    comment: Optional[str] = None

    @validator("rating")
    def clamp(cls, v):
        if v > 5:
            return 5
        elif v < 0:
            return 0
        return v


class RatingReturn(BaseModel):
    id: Optional[int] = 1
    user: UserRef
    application: ApplicationRef
    rating: float
    comment: Optional[str] = None
    updated: Optional[datetime] = None


class RatingAverage(BaseModel):
    application: ApplicationRef
    rating: Optional[float] = 0


class Message(BaseModel):
    msg: Optional[str] = "success"


class Count(BaseModel):
    count: Optional[int] = 0