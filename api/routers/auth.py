# FastAPI
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, Response, JSONResponse
from starlette.requests import Request

# SQLAlchemy
from sqlalchemy.orm import Session

# Types
from typing import List

# Custom Modules
from .. import schemas, crud
from ..core import security
from ..core.config import settings
from ..dependencies import get_db, get_current_user

import os

router = APIRouter(tags=['auth'])


@router.post("/token")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """User will attempt to authenticate with a email/password flow
    """

    user = security.authenticate_user(
        db, form_data.username, form_data.password)
    if not user:
        # Wrong email or password provided
        raise HTTPException(
            status_code=401, detail="Incorrect username or password")

    if user.account_verified == False:
        raise HTTPException(
            status_code=400, detail="Email is not verified. Please check your email.")

    token = security.create_access_token(data={"sub": user.email})
    response.set_cookie(
        key="Authorization",
        value=f'Bearer {token}',
        samesite="Lax" if "dev" in os.environ.get("ENV") else "None",
        domain="localhost"
        if "dev" in os.environ.get("ENV")
        else "dericfagnan.com",
        secure="dev" not in os.environ.get("ENV"),
        httponly=True,
        max_age=60 * 30,
        expires=60 * 30,
    )

    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
async def logout_and_expire_cookie(response: Response, current_user: schemas.User = Depends(get_current_user)):
    # response.delete_cookie("Authorization")
    response.set_cookie(
        key="Authorization",
        value=f'',
        samesite="Lax" if "dev" in os.environ.get("ENV") else "None",
        domain="localhost"
        if "dev" in os.environ.get("ENV")
        else "dericfagnan.com",
        secure="dev" not in os.environ.get("ENV"),
        httponly=True,
        max_age=1,
        expires=1,
    )

    return {}
