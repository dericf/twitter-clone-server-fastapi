from typing import List, Optional, ForwardRef, Generic, Any
from pydantic import BaseModel

from datetime import datetime, date

from . import BasicUser


class Follow(BaseModel):
    user: BasicUser
    followsUser: BasicUser


class FollowsCreateRequestBody(BaseModel):
    followUserId: int


class FollowsDeleteRequestBody(BaseModel):
    followUserId: int


class FollowsResponse(BaseModel):
    userId: int
    email: str
    username: str
    bio: str
    birthdate: date

    class Config:
        orm_mode = True


class WSFollowsUpdateBody(BaseModel):
    userId: int
    followUserId: int
