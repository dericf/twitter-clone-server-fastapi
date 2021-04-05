from typing import List, Optional
from datetime import datetime, date

from pydantic import BaseModel

class CommentBase(BaseModel):
    id: Optional[int]
    userId: int
    tweetId: int
    content: str

class Comment(CommentBase):
    # tweet: List[Tweet] = []
    class Config:
        orm_mode = True

class CommentCreate(BaseModel):
    content: str
    tweetId: int

class CommentDelete(BaseModel):
    commentId: int

class CommentUpdate(BaseModel):
    commentId: int
    newContent: str