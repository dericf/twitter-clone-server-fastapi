from typing import List, Optional, ForwardRef, Generic, Any
from pydantic import BaseModel

from datetime import datetime, date

from . import BasicUser

class Follower(BaseModel):
    user: BasicUser
    followsUser: BasicUser

    class Config:
        orm_mode = True
    

class FollowersRequestBody(BaseModel):
    userId: int

class FollowersResponse(BaseModel):
    userId: int
    email: str
    username: str
    bio: str
    birthdate: date
    