from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..core import security
from ..core.config import settings
from ..dependencies import get_db

router = APIRouter(prefix="/comments", tags=['comments'])

@router.post("/", response_model=schemas.Comment)
def create_comment_for_tweet(
    comment: schemas.CommentCreate, db: Session = Depends(get_db)
):
    return crud.create_tweet_comment(db=db, comment=comment)

@router.put("/", response_model=schemas.Comment)
def update_comment(
    comment: schemas.CommentUpdate, db: Session = Depends(get_db)
):
    return crud.update_commentnt(db=db, comment=comment)

@router.get("/user/{user_id}/", response_model=List[schemas.Comment])
def get_comments_for_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = crud.get_comments_for_user(db, user_id=user_id, skip=skip, limit=limit)
    return comments

@router.get("/tweet/{tweet_id}/", response_model=List[schemas.Comment])
def get_comments_for_tweet(tweet_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = crud.get_comments_for_tweet(db, tweet_id=tweet_id, skip=skip, limit=limit)
    return comments