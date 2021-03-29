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
from ..dependencies import get_db

router = APIRouter(tags=['auth'])


@router.post("/token")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """User will attempt to authenticate with a email/password flow
    """
    try:
        user = security.authenticate_user(
        db, form_data.username, form_data.password)
        if not user:
            # Wrong email or password provided
            raise HTTPException(
                status_code=400, detail="Incorrect username or password")

        token = security.create_access_token(data={"sub": user.email})
        response.set_cookie(
            key="Authorization", 
            value=f'Bearer {token}', 
            samesite="None",
            secure=True,
            httponly=True, 
            max_age=1800,
            expires=1800
        )
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        response = Response(headers={"WWW-Authenticate": "Basic"}, status_code=401)
        return response