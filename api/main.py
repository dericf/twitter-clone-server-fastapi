# Standard Library
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
from .core.config import settings
from .core import security
from .database import SessionLocal, engine
from . import crud, models, schemas, dependencies
from sqlalchemy.orm import Session
from typing import List, Dict, Union
from fastapi.middleware.cors import CORSMiddleware
import os
import time
import json

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

# Types

# SQLAlchemy

# Custom Modules
from .core.websocket.connection_manager import ws_manager

# Import all routers defined in other modules

app = FastAPI(
    # root_path=settings.API_V1_STR,
    title="Twitter Clone (For Educational Purposes)",
    description="This API replicates some of the very basic functionality of twitter, including users, tweets, likes, comments and",
    version="0.0.1",
)

# C.O.R.S.
origins = [
    "http://localhost",
    "ws://localhost",
    "ws://localhost:8080",
    "http://localhost:8080",
    "http://localhost:3000",  # Frontend NextJS Client
    # Production Client on Vercel HTTP
    "http://twitter-clone-frontend-beryl.vercel.app",
    "https://twitter-clone-frontend-beryl.vercel.app",  # Production Client on Vercel
    # Alternate Production Client on Vercel HTTP
    "http://twitter-clone.projects.programmertutor.com",
    # Alternate Production Client on Vercel
    "https://twitter-clone.programmertutor.com",
    "https://www.twitter-clone.programmertutor.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
    # print("\n********************\nNew Websocket Connection Incoming: ")
    # print("user_id: ", user_id)
    # print("current user", current_user)
    await ws_manager.show_all_connections()
    #
    # Attempt to connect new client
    #
    await ws_manager.connect(websocket, user_id)
    if not current_user:
        # print("No authenticated user - Alert client and close connection...")
        auth_failed_message = {
            "action": "auth.required",
            "message": "Authentication failed",
            "status": 401
        }
        await ws_manager.send_personal_message(auth_failed_message, user_id)
        await ws_manager.disconnect(user_id)
    # await ws_manager.send_personal_message({
    #     "message": "Connection OK",
    #     "status": 200
    # }, user_id)
    #
    # New client has connected
    #
    user: schemas.User = crud.get_user_by_id(db, user_id)
    # await ws_manager.broadcast({"action": "notification", "message": f"{user.username} joined the chat"})

    try:
        while True:
            #
            # Receive incoming message
            #
            data = await websocket.receive_json()

            user: schemas.User = crud.get_user_by_id(db, user_id)
            # data = json.loads(data)
            print("\n*************** New Websocket Message *************")
            print(f"user: {user} ")

            action = data.get("action")
            print("Action: ", action)

    except WebSocketDisconnect as error:
        #
        # Client has disconnected
        #
        # print("Client Disconnected !: ", error)
        await ws_manager.disconnect(user_id)
        await ws_manager.broadcast({"action": "notification", "message": f"{user.username} disconnected"})
