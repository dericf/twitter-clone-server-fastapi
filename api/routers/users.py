# FastAPI
from fastapi import APIRouter, HTTPException, Request, Depends

# SQLAlchemy
from sqlalchemy.orm import Session

# Types
from typing import List

# Custom Modules
from .. import schemas, crud, dependencies
from ..core import security
from ..core.config import settings
from ..dependencies import get_db

router = APIRouter(prefix="/users", tags=['users'])


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user record in the database
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=List[schemas.UserResponse])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Return a list of all users in the database
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    #
    # Example of building a custom pydantic model
    #
    return [schemas.UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        bio=user.bio,
        birthdate=user.birthdate,
        tweets=[
            schemas.BasicTweet(
                id=tweet.id,
                content=tweet.content
            ) for tweet in user.tweets
        ]
    ) for user in users]


@router.get("/me", response_model=schemas.User)
def get_authenticated_user(db: Session = Depends(get_db), current_user: schemas.User = Depends(dependencies.get_current_user)):
    """Get the currently logged in user if there is one (testing purposes only)
    """
    return current_user


@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Return a single user based on user_id primary key
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
