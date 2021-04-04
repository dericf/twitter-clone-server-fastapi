from typing import List, Optional
from datetime import datetime, date

from pydantic import BaseModel

class CommentBase(BaseModel):
    id: Optional[int]
    userId: int
    tweet_id: int
    content: str

class Comment(CommentBase):
    # tweet: List[Tweet] = []
    class Config:
        orm_mode = True

class CommentCreate(BaseModel):
    content: str
    tweet_id: int

class CommentDelete(BaseModel):
    comment_id: int

class CommentUpdate(BaseModel):
    comment_id: int
    new_content: str