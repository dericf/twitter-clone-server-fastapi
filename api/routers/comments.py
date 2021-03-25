from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..core import security
from ..core.config import settings
from ..dependencies import get_db, get_current_user

router = APIRouter(prefix="/comments", tags=['comments'])


@router.get("/user/{user_id}/", response_model=List[schemas.Comment])
def get_comments_for_user(
    user_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    comments = crud.get_comments_for_user(db, user_id=user_id, skip=skip, limit=limit)
    return comments


@router.get("/tweet/{tweet_id}/", response_model=List[schemas.Comment])
def get_comments_for_tweet(
    tweet_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    comments = crud.get_comments_for_tweet(db, tweet_id=tweet_id, skip=skip, limit=limit)
    return comments


@router.post("/", response_model=schemas.Comment)
def create_comment_for_tweet(
    request_body: schemas.CommentCreate, 
    db: Session = Depends(get_db),
    current_user: schemas.UserWithPassword = Depends(get_current_user)
):
    return crud.create_tweet_comment(db, current_user.id, request_body)


@router.put("/", response_model=schemas.Comment)
def update_comment(
    request_body: schemas.CommentUpdate, 
    db: Session = Depends(get_db),
    current_user: schemas.UserWithPassword = Depends(get_current_user)
):
    return crud.update_comment(db, current_user.id, request_body)


@router.delete("/", response_model=schemas.EmptyResponse)
def delete_comment(
    request_body: schemas.CommentDelete, 
    db: Session = Depends(get_db),
    current_user: schemas.UserWithPassword = Depends(get_current_user)
):
    return crud.delete_comment(db, current_user.id, request_body)