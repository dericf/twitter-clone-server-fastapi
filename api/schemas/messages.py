from typing import List, Optional
from datetime import datetime, date

from pydantic import BaseModel


class Message(BaseModel):
    id: Optional[int]
    userFromId: int
    userFromUsername: str
    userToId: int
    userToUsername: str
    content: str
    createdAt: datetime


class Conversation(BaseModel):
    List[Message]


class MessageResponse(BaseModel):
    conversations: List[Conversation]


class MessageCreateRequestBody(BaseModel):
    content: str
    userToId: int


class MessageDeleteRequestBody(BaseModel):
    messageId: int


class MessageUpdateRequestBody(BaseModel):
    messageId: int
    newContent: str
