from typing import List, Optional, ForwardRef, Generic, Any
from pydantic import BaseModel

from datetime import datetime, date


class BasicTweet(BaseModel):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class BasicUser(BaseModel):
    id: int
    email: str
    username: str
    bio: Optional[str]

    class Config:
        orm_mode = True

class TweetLikeCreateResponseBody(BaseModel):
    tweetId: int
    userId: int
    username: str

class TweetLikeResponseBody(BaseModel):
    tweetId: int
    userId: int
    username: str


class TweetLike(BaseModel):
    tweetId: int
    tweet: BasicTweet
    userId: BasicUser

    class Config:
        orm_mode = True

class TweetLikeCreateRequestBody(BaseModel):
    tweetId: Optional[int]