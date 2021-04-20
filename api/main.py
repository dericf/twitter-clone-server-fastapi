# Standard Library
import os
import time

# FastAPI
from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware

# Types
from typing import List

# SQLAlchemy
from sqlalchemy.orm import Session

# Custom Modules
from . import crud, models, schemas, dependencies
from .database import SessionLocal, engine
from .core import security
from .core.config import settings

# Import all routers defined in other modules
from .routers import auth, users, tweets, comments, followers, follows, tweet_likes, comment_likes

app = FastAPI(
    # root_path=settings.API_V1_STR,
    title="Twitter Clone (For Educational Purposes)",
    description="This API replicates some of the very basic functionality of twitter, including users, tweets, likes, comments and",
    version="0.0.1",
)

# C.O.R.S.
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",  # Frontend NextJS Client
    # Production Client on Vercel HTTP
    "http://twitter-clone-frontend-beryl.vercel.app",
    "https://twitter-clone-frontend-beryl.vercel.app",  # Production Client on Vercel
    # Alternate Production Client on Vercel HTTP
    "http://twitter-clone.projects.programmertutor.com",
    # Alternate Production Client on Vercel
    "https://twitter-clone.programmertutor.com",
    "https://www.twitter-clone.programmertutor.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["set-cookie"]
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
    """Index route. Only used for testing purposes.
    """
    return {"api_status": "ok"}
