from typing import List, Optional
from datetime import datetime, date

from pydantic import BaseModel

from .users import UserBase

class BasicUser(UserBase):
    id: int

    class Config:
        orm_mode = True