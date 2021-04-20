# Standard Library
from datetime import datetime, date

# Types
from typing import List, Optional, Any
from pydantic import BaseModel, validator


class CountBase(BaseModel):
    count: int


class TweetCommentCount(CountBase):
    """The number of comments for a given tweet
    """
    pass
