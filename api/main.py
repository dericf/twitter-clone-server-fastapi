# Standard Library
import os

# FastAPI
from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks, Request

# Types
from typing import List

# SQLAlchemy
from sqlalchemy.orm import Session

# Custom Modules
from . import crud, models, schemas, dependencies, background_tasks as background_utilities
from .database import SessionLocal, engine
from .core import security
from .core.config import settings

# Import all routers defined in other modules
from .routers import auth, users, tweets, comments

app = FastAPI(
    # root_path=settings.API_V1_STR,
    title="Twitter Clone (For Educational Purposes)",
    description="This API replicates some of the very basic functionality of twitter, including users, tweets, likes, comments and",
    version="0.0.1",
)

# Include All Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tweets.router)
app.include_router(comments.router)


@app.get("/")
def index(request: Request):
    """Index route. Only used for testing purposes.
    """
    return {"api_status": "ok"}
