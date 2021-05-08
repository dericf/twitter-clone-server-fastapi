from typing import List, Optional
from datetime import datetime, date

from pydantic import BaseModel

from . import Message


class ChatUserOnlineRequestBody(BaseModel):
    userId: int


class ChatUserOnlineResponseBody(BaseModel):
    userId: Optional[int]
    username: Optional[str]
    isOnline: bool


class ChatUserTypingRequestBody(BaseModel):
    userId: int  # other user


class ChatUserTypingResponseBody(BaseModel):
    isTyping: bool


class NewChatMessageResponseBody(Message):
    # Just a message
    pass


class DeletedChatMessageResponseBody(BaseModel):
    messageId: int
    userId: int
