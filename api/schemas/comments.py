from typing import List, Optional
from datetime import datetime, date

from pydantic import BaseModel

class CommentBase(BaseModel):
    id: Optional[int]
    user_id: int
    tweet_id: int
    content: str

class Comment(CommentBase):
    # tweet: List[Tweet] = []
    class Config:
        orm_mode = True

class CommentCreate(CommentBase):
    pass

class CommentUpdate(CommentBase):
    new_content: str