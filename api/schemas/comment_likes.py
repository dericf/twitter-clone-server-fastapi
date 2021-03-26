from typing import List, Optional, ForwardRef, Generic, Any
from pydantic import BaseModel

from datetime import datetime, date


class BasicComment(BaseModel):
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

class CommentLikeCreateResponseBody(BaseModel):
    commentId: int
    userId: int
    username: str

class CommentLikeResponseBody(BaseModel):
    commentId: int
    userId: int
    username: str


class CommentLike(BaseModel):
    commentId: int
    comment: BasicComment
    userId: BasicUser

    class Config:
        orm_mode = True

class CommentLikeCreateRequestBody(BaseModel):
    commentId: Optional[int]

class CommentLikeDeleteRequestBody(BaseModel):
    commentId: int