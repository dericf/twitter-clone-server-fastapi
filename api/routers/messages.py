# FastAPI
from fastapi import (
    APIRouter, HTTPException, status,
    Request, Depends, BackgroundTasks,
    WebSocket, WebSocketDisconnect, Cookie, Query
)
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder

# SQLAlchemy
from sqlalchemy.orm import Session

# Types
from typing import List, Optional

# Custom Modules
from .. import schemas, crud, models
from ..background_functions.email_notifications import send_new_message_notification_email
from ..dependencies import get_db, get_current_user
from ..core import security
from ..core.config import settings
from ..core.utilities import generate_random_uuid
from ..core.websocket.connection_manager import ws_manager

# Schema
from ..schemas.websockets import WSMessage, WSMessageAction
from ..core.sendgrid.schema import EmailSender

router = APIRouter(prefix="/messages", tags=['messages'])


@router.get("/conversations")
# respone_model=schemas.MessageResponse
def messages(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):

    return crud.get_messages_for_user(db, current_user.id)


@router.get("")
# respone_model=schemas.MessageResponse
def messages(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):

    messages = crud.get_messages_for_user(db, current_user.id)
    return [schemas.Message(
        id=message.id,
        userFromId=message.user_from_id,
        userFromUsername=message.user_from.username,
        userToId=message.user_to_id,
        userToUsername=message.user_to.username,
        content=message.content,
        createdAt=message.created_at
    ) for message in messages]


@router.post("", response_model=schemas.Message)
async def create_message(
    request_body: schemas.MessageCreateRequestBody,
    bg_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    newMessage = crud.create_message(db, current_user.id, request_body)
    return_value = schemas.Message(
        id=newMessage.id,
        userFromId=newMessage.user_from_id,
        userFromUsername=current_user.username,
        userToId=newMessage.user_to_id,
        userToUsername=newMessage.user_to.username,
        content=newMessage.content,
        createdAt=newMessage.created_at
    )
    other_user = crud.get_user_by_id(db, newMessage.user_to_id)
    # Send a websocket message to the user who this message is sent to
    # If that user is not online, they will not receive the websocket message.
    wsMessage = WSMessage[schemas.Message](
        action=WSMessageAction.ChatMessageNew,
        body=return_value
    )
    if ws_manager.user_is_online(request_body.userToId):
        print('user is online')
        await ws_manager.send_personal_message(wsMessage, request_body.userToId)
    else:
        print("sending a notification email")
        # Send an email notification to the user.
        # TODO - perhaps implement some rate limiting here so it only sends
        #        a max amount per minute or something.
        #        this could be another dict holding last time sent...?
        bg_tasks.add_task(send_new_message_notification_email,
                          current_user, other_user)

    return return_value


@router.delete("/", response_model=schemas.EmptyResponse)
async def delete_message(
    request_body: schemas.MessageDeleteRequestBody,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    message: models.Messages = crud.get_message_by_id(
        db, request_body.messageId)
    result = crud.delete_message(db, current_user.id, request_body)

    # Send a websocket message to the user who this message is sent to
    # If that user is not online, they will not receive the websocket message.
    wsMessage = WSMessage[schemas.DeletedChatMessageResponseBody](
        action=WSMessageAction.ChatMessageDeleted,
        body=schemas.DeletedChatMessageResponseBody(
            messageId=request_body.messageId,
            userId=message.user_from_id
        )
    )

    if ws_manager.user_is_online(message.user_from_id):
        await ws_manager.send_personal_message(wsMessage, message.user_to_id)

    return result
