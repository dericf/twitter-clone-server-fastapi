import os
from typing import List

from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks, Request
from sqlalchemy.orm import Session

from . import crud, models, schemas, dependencies, background_tasks
from .database import SessionLocal, engine
from .core import security
from .core.config import settings

from .routers import auth, users, tweets, comments
# models.Base.metadata.create_all(bind=engine)

##
# - TODO: Add dockerignore file
##
app = FastAPI(
    # root_path=settings.API_V1_STR,
    title="Twitter Clone (Educational)",
    description="",
    version="0.0.1",
    # openapi_url="/api/v1/openapi.json"
)

# Include All Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tweets.router)
app.include_router(comments.router)


@app.get("/")
def index(request: Request):
    print(request.scope.get("root_path"))
    return {"status": "ok"}

@app.post("/send-notification/{email}")
def send_notification(email: str, background_tasks: BackgroundTasks):
    """Initialize Background Task: Send Email Notification
    TODO: add validation first (and likely other params)
    """
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}