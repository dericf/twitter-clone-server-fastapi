from typing import List, Optional, ForwardRef, Generic, Any
from pydantic import BaseModel

from datetime import datetime, date


from .tweets import TweetBase

class BasicTweet(TweetBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
