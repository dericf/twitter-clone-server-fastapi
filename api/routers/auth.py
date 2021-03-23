from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..core import security
from ..core.config import settings
from ..dependencies import get_db

router = APIRouter(prefix="/auth", tags=['auth'])


@router.post('/login', response_model=schemas.LoginResponse)
def attempt_login(request: Request, body:schemas.LoginRequest):
    print(request.json)
    print("Email: ")
    print(body.email)
    user: schemas.User = crud.get_user_by_email(email=body.email)
    if not user:
        return schemas.LoginResponse(success=False, error=True, message="")
    print(security.verify_password(body.password, user.password))
    return schemas.LoginResponse(success=True)