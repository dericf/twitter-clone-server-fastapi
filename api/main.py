# Standard Library
import os
import time
import json
from typing import List, Dict, Union

# FastAPI
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    BackgroundTasks,
    Request,
    WebSocket,
    WebSocketDisconnect,
    Cookie,
    Query,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

# Routers
from .routers import (
    auth,
    users,
    tweets,
    comments,
    followers,
    follows,
    tweet_likes,
    comment_likes,
    messages,
)

# SQLAlchemy
from sqlalchemy.orm import Session

# Core
from .core import security
from .core.config import settings
from .core.cors import cors_origins
from .core.websocket.connection_manager import ws_manager

# Database
from .database import SessionLocal, engine
from . import crud, models, schemas, dependencies

# Schema
from .schemas.websockets import WSMessage, WSMessageAction, WSMessageError

# Instantiate Main FastAPI Instance
app = FastAPI(
    # root_path=settings.API_V1_STR,
    title="Twitter Clone (For Educational Purposes)",
    description="This API replicates some of the very basic functionality of twitter, including users, tweets, likes, comments and",
    version="0.0.1",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["set-cookie"],
)

# Include All Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tweets.router)
app.include_router(comments.router)
app.include_router(follows.router)
app.include_router(followers.router)
app.include_router(tweet_likes.router)
app.include_router(comment_likes.router)
app.include_router(messages.router)

# Needed to resolve an unknown http bug


@app.middleware("http")
async def modify_location_header(request: Request, call_next):
    """This is a very hacky fix for a glitch in the "location" response header
    For some reason it sends back http instead of https so I manually
    overwrite it here. Definitely something that should be fixed upstream in
    configuration but this will work temporarily until I find the correct location.
    """
    response: Response = await call_next(request)

    # Check for location response header
    location = response.headers.get("location")
    if location and os.environ.get("ENV") != "development":
        response.headers["location"] = location.replace("http:", "https:")
    return response

# Dummy route at the index


@app.get("/")
def index(request: Request):
    """Index route. Only used for testing purposes."""
    return {"api_status": "ok"}


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int,
    db: Session = Depends(dependencies.get_db),
    current_user: schemas.User = Depends(dependencies.get_current_user)
):
    """
    Websocket endpoint for authenticated users.

    Listens for incoming CONNECTIONS and uses the connection_manager class to
    update the dictionary of active connections.

    Listens for incoming MESSAGES and handles them accordingly

    TODO: This should be moved to its own websocket module
    TODO: The /user_id param should not be needed anymore since it gets it from the token
    """
    # print("\n********************\nNew Websocket Connection Incoming: ")
    # print("user_id: ", user_id)
    # print("current user", current_user)
    # await ws_manager.show_all_connections()
    #
    # Attempt to connect new client
    #
    await ws_manager.connect(websocket, user_id)
    if not current_user:
        # print("No authenticated user - Alert client and close connection...")
        auth_failed_message = WSMessage[None](
            action=WSMessageAction.AuthRequired,
            message="error",
            error=WSMessageError(
                message="Authentication failed",
                code=401
            )
        )
        await ws_manager.send_personal_message(auth_failed_message, user_id)
        await ws_manager.disconnect(user_id)
        return
    #
    # New client has connected
    #
    # user: schemas.User = crud.get_user_by_id(db, user_id)
    await ws_manager.broadcast({"action": "chat.user.online", "body": jsonable_encoder(
        schemas.ChatUserOnlineResponseBody(
            isOnline=True,
            userId=user_id,
            username=current_user.username
        )
    )}, user_id)

    try:
        while True:
            #
            # Receive incoming message
            # ! Note: so far the client does not send any WS messages - instead relies on the http rest api
            data = await websocket.receive_json()

            user: schemas.User = crud.get_user_by_id(db, user_id)

            # data = json.loads(data)
            # print("\n*************** New Websocket Message *************")
            # print(data)
            # print(f"user: {user} ")
            action = data.get("action")

            if (action == "chat.user.online"):
                body = schemas.ChatUserOnlineRequestBody(**data.get("body"))
                # print("Action: ", action)
                response_body = schemas.ChatUserOnlineResponseBody(
                    isOnline=ws_manager.user_is_online(body.userId),
                    userId=body.userId
                )
                # Send a message back to notify if the other user is online or not
                await websocket.send_json(
                    {"action": action, "body": jsonable_encoder(response_body)})

            elif (action == "chat.user.typing"):
                body = schemas.ChatUserTypingRequestBody(**data.get("body"))
                response_body = schemas.ChatUserTypingResponseBody(
                    isTyping=True
                )

                await ws_manager.send_personal_message(
                    {"action": action, "body": jsonable_encoder(response_body)}, body.userId)

    except WebSocketDisconnect as error:
        #
        # Client has disconnected
        #
        # print("Client Disconnected !: ", error)
        await ws_manager.broadcast({"action": "chat.user.online", "body": jsonable_encoder(
            schemas.ChatUserOnlineResponseBody(
                isOnline=False,
                userId=user_id,
                username=current_user.username
            )
        )}, user_id)
        await ws_manager.disconnect(user_id)
        # await ws_manager.broadcast({"action": "notification", "message": f"{user.username} disconnected"})
