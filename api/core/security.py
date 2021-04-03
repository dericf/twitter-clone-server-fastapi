# Standard Library
from datetime import datetime, timedelta

# Types
from typing import Any, Union, Optional

# SQLAlchemy
from sqlalchemy.orm import Session

# JWT
from jose import jwt, JWTError

# Hashing
from passlib.context import CryptContext

# Custom Modules
from .config import settings
from ..schemas import User
from .. import crud

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT (access token) based on the provided data
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check that hashed(plain_password) matches hashed_password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Return the hashed version of password
    """
    return pwd_context.hash(password)


def decode_token(token: str):
    """Return a dictionary that represents the decoded JWT.
    """
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])


def authenticate_user(db: Session, email: str, password: str) -> Union[bool, User]:
    """Based on the provided email & password, verify that the credentials match
    the records contained in the database.
    """
    user = crud.get_user_by_email_or_username(db, email)
    if not user:
        # No user with that email exists in the database
        return False
    if not verify_password(password, user.hashed_password):
        # The user exists but the password was incorrect
        return False
    return user
