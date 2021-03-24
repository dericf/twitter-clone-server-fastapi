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


class BasicTweet(BaseModel):
    id: int
    content: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    bio: Optional[str]
    birthdate: Optional[date]
    tweets: Optional[List[BasicTweet]] = []
