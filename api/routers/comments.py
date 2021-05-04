from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..core import security
from ..core.config import settings
from ..dependencies import get_db, get_current_user

router = APIRouter(prefix="/comments", tags=['comments'])


@router.get("/user/{userId}/", response_model=List[schemas.Comment])
def get_comments_for_user(
    userId: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    comments = crud.get_comments_for_user(
        db, user_id=userId, skip=skip, limit=limit)
    return [
        schemas.Comment(
            id=comment.id,
            userId=comment.user_id,
            tweetId=comment.tweet_id,
            content=comment.content,
            username=comment.user.username,
            createdAt=comment.created_at
        ) for comment in comments
    ]


@router.get("/tweet/{tweetId}/", response_model=List[schemas.Comment])
def get_comments_for_tweet(
    tweetId: int,
    skip: int = 0,
    limit: int = 0,
    db: Session = Depends(get_db)
):
    comments = crud.get_comments_for_tweet(
        db, tweet_id=tweetId, skip=skip, limit=limit)
    return [
        schemas.Comment(
            id=comment.id,
            userId=comment.user_id,
            tweetId=comment.tweet_id,
            content=comment.content,
            username=comment.user.username,
            createdAt=comment.created_at
        ) for comment in comments
    ]


@router.get("/count/tweet/{tweetId}/", response_model=schemas.TweetCommentCount)
def get_comment_count_for_tweet(
    tweetId: int,
    db: Session = Depends(get_db)
):
    count = crud.get_comment_count_for_tweet(db, tweet_id=tweetId)

    return schemas.TweetCommentCount(
        count=count
    )


@router.post("/", response_model=schemas.Comment)
def create_comment_for_tweet(
    request_body: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    newComment = crud.create_tweet_comment(db, current_user.id, request_body)
    return schemas.Comment(
        id=newComment.id,
        userId=newComment.user_id,
        tweetId=newComment.tweet_id,
        content=newComment.content,
        username=newComment.user.username,
        createdAt=newComment.created_at
    )


@router.put("/", response_model=schemas.Comment)
def update_comment(
    request_body: schemas.CommentUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    comment = crud.update_comment(db, current_user.id, request_body)

    return schemas.Comment(
        id=comment.id,
        userId=comment.user_id,
        tweetId=comment.tweet_id,
        content=comment.content,
        username=comment.user.username,
        createdAt=comment.created_at
    )


@router.delete("/", response_model=schemas.EmptyResponse)
def delete_comment(
    request_body: schemas.CommentDelete,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.delete_comment(db, current_user.id, request_body)
