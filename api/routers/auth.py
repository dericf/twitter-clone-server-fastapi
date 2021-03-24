# FastAPI
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm

# SQLAlchemy
from sqlalchemy.orm import Session

# Types
from typing import List

# Custom Modules
from .. import schemas, crud
from ..core import security
from ..core.config import settings
from ..dependencies import get_db

router = APIRouter(tags=['auth'])


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """User will attempt to authenticate with a email/password flow
    """
    user = security.authenticate_user(
        db, form_data.username, form_data.password)
    if not user:
        # Wrong email or password provided
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    token = security.create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
