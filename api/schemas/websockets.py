from enum import Enum
from typing import List, Optional, Generic, TypeVar
from datetime import datetime, date

from pydantic import BaseModel
from pydantic.generics import GenericModel


class WSMessageAction(str, Enum):
    ChatMessageNew = "chat.message.new"
    ChatMessageDeleted = "chat.message.deleted"
    ChatUserOnline = "chat.user.online"
    ChatUserTyping = "chat.user.typing"
    AuthRequired = "auth.required"
    NewFollower = "followers.followed"
    LostFollower = "followers.unfollowed"
    NewComment = "comments.new"
    DeletedComment = "comments.deleted"
    UpdatedComment = "comments.updated"
    UpdatedCommentLike = "comments.likes.changed"
    UpdatedTweetLike = "tweets.likes.changed"


WSMessageBody = TypeVar("WSBody")


class WSMessageError(BaseModel):
    code: int
    message: str

# WSAction =


class WSMessage(GenericModel, Generic[WSMessageBody]):
    action: WSMessageAction
    body: WSMessageBody
    status: Optional[int]
    error: Optional[WSMessageError]
