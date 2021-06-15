from typing import List, Optional
from datetime import datetime, date

from pydantic import BaseModel, AnyHttpUrl, EmailStr, HttpUrl, validator


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = False


class LoginResponse(BaseModel):
    success: Optional[bool]
    error: Optional[bool]
    message: Optional[str] = None

    class Config:
        orm_mode = False


class LogoutResponse(BaseModel):
    success: bool
    error: bool
    message: Optional[str] = None

    class Config:
        orm_mode = False


class RegisterResponse(BaseModel):
    success: bool
    error: bool
    message: Optional[str] = None

    class Config:
        orm_mode = False
