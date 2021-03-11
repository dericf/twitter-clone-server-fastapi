from typing import List, Optional
from datetime import datetime, date

from pydantic import BaseModel


class TweetBase(BaseModel):
    content: str
    

class TweetCreate(TweetBase):
    pass


class Tweet(TweetBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    username: str
    bio: Optional[str]
    birthdate: Optional[date]


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    tweets: List[Tweet] = []

    class Config:
        orm_mode = True