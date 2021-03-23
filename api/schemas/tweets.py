from typing import List, Optional, ForwardRef, Generic, Any
from pydantic import BaseModel

from datetime import datetime, date


class TweetBase(BaseModel):
    content: str
    

class TweetCreate(TweetBase):
    pass


class Tweet(TweetBase):
    id: int

    class Config:
        orm_mode = True

class TweetResponse(BaseModel):
    tweetId: int
    userId: int
    username: str
    content: str
    createdAt: datetime