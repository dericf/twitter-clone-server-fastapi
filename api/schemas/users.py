# Standard Library
from datetime import datetime, date

# Types
from typing import List, Optional, Any
from pydantic import BaseModel, validator

# SQLAlchemy
from sqlalchemy.orm import Query


class UserBase(BaseModel):
    email: str
    username: str
    bio: Optional[str]
    birthdate: Optional[date]


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserWithPassword(User):
    hashed_password: str

    class Config:
        orm_mode = True


class UserDeleteRequestBody(BaseModel):
    password: str


class UserUpdateResponseBody(BaseModel):
    id: int
    email: str
    username: str
    bio: Optional[str]
    birthdate: Optional[date]

    class Config:
        orm_mode = True


class UserUpdateRequestBody(BaseModel):
    password: str
    newUsername: Optional[str]
    newBio: Optional[str]


class BasicTweet(BaseModel):
    id: int
    content: str
    createdAt: datetime


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    bio: Optional[str]
    birthdate: Optional[date]
    # tweets: Optional[List[BasicTweet]] = []


class UserAccountConfirmationRequestBody(BaseModel):
    confirmationKey: str
