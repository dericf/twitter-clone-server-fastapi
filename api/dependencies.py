# FastAPI
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

# SQLAlchemy
from sqlalchemy.orm.session import Session

# JWT
from jose import JWTError, jwt

# Custom Modules
from . import crud, schemas
from .database import SessionLocal
from .core import security
from .core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    """Yield a SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Decode the provided jwt and extract the user using the [sub] field.
    """
    token_data: schemas.TokenData = None

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security.decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            # Something wrong with the token
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        # Something wrong with the token
        raise credentials_exception
    #
    # Get user from database
    #
    user = crud.get_user_by_email(db, token_data.email)
    if user is None:
        raise credentials_exception
    return user
