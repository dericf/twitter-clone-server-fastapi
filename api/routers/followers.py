# FastAPI
from fastapi import APIRouter, HTTPException, Request, Depends, status

# SQLAlchemy
from sqlalchemy.orm import Session

# Types
from typing import List, Optional

# Custom Modules
from .. import schemas, crud
from ..dependencies import get_db, get_current_user
from ..core import security
from ..core.config import settings

# FastAPI router object
router = APIRouter(prefix="/followers", tags=['followers'])


@router.get("/{userId}", response_model=List[schemas.FollowersResponse])
def get_all_tweets(userId: int, db: Session = Depends(get_db)):
    """
    The GET method for this endpoint requires a userId and will send 
    back information about all users the follow that user. 

    This endpoint will always return an array of objects. 
    """
    followers: List[schemas.Follower] = crud.get_all_followers(db, userId)
    return [
        schemas.FollowersResponse(
            userId=follower.user.id,
            email=follower.user.email,
            username=follower.user.username,
            bio=follower.user.bio,
            birthdate=follower.user.birthdate
        ) for follower in followers
    ]


@router.get("/count/{userId}", response_model=schemas.CountBase)
def get_followers_count_for_user(
    userId: int,
    db: Session = Depends(get_db)
):
    count = crud.get_followers_for_user(db, user_id=userId)

    return schemas.CountBase(
        count=count
    )
