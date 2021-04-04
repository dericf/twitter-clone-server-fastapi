from typing import List, Optional, ForwardRef, Generic, Any
from pydantic import BaseModel

from datetime import datetime, date


class TweetBase(BaseModel):
    content: str
    

class TweetCreate(TweetBase):
    pass

class TweetUpdate(BaseModel):
    newContent: str


class Tweet(TweetBase):
    id: int
    userId: int
    username: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True

class TweetResponse(BaseModel):
    tweetId: int
    userId: int
    username: str
    content: str
    createdAt: datetime