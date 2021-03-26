from typing import List, Optional, ForwardRef, Generic, Any
from pydantic import BaseModel

from datetime import datetime, date

class BasicTweet(BaseModel):
    id: int
    user_id: int

    class Config:
        orm_mode = True
