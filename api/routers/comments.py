from fastapi import APIRouter, HTTPException, Request, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..core import security
from ..core.config import settings
from ..core.websocket.connection_manager import ws_manager
from ..dependencies import get_db, get_current_user
from ..background_functions.email_notifications import send_new_comment_notification_email
from ..schemas.websockets import WSMessage, WSMessageAction

router = APIRouter(prefix="/comments", tags=['comments'])


@router.get("/user/{userId}", response_model=List[schemas.Comment])
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


@router.get("/tweet/{tweetId}", response_model=List[schemas.Comment])
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


@router.get("/count/tweet/{tweetId}", response_model=schemas.TweetCommentCount)
def get_comment_count_for_tweet(
    tweetId: int,
    db: Session = Depends(get_db)
):
    count = crud.get_comment_count_for_tweet(db, tweet_id=tweetId)

    return schemas.TweetCommentCount(
        count=count
    )


@router.post("", response_model=schemas.Comment)
async def create_comment_for_tweet(
    request_body: schemas.CommentCreate,
    bg_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    newComment = crud.create_tweet_comment(db, current_user.id, request_body)

    # Broadcast a WS message so users can see the new comment get updated in real-time
    return_comment = schemas.Comment(
        id=newComment.id,
        userId=newComment.user_id,
        tweetId=newComment.tweet_id,
        content=newComment.content,
        username=newComment.user.username,
        createdAt=newComment.created_at
    )
    message = WSMessage[schemas.WSCommentCreated](
        action=WSMessageAction.NewComment,
        body=schemas.WSCommentCreated(
            comment=return_comment
        )
    )

    if not ws_manager.user_is_online(newComment.tweet.user.id):
        bg_tasks.add_task(send_new_comment_notification_email,
                          tweet_owner=newComment.tweet.user, commenter=newComment.user, comment=newComment)

    # Push the new comment to all online users
    await ws_manager.broadcast(message, current_user.id)
    return return_comment


@router.put("", response_model=schemas.Comment)
async def update_comment(
    request_body: schemas.CommentUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    comment = crud.update_comment(db, current_user.id, request_body)
    return_comment = schemas.Comment(
        id=comment.id,
        userId=comment.user_id,
        tweetId=comment.tweet_id,
        content=comment.content,
        username=comment.user.username,
        createdAt=comment.created_at
    )
    #
    # Broadcast a WS message so users can see the new comment get updated in real-time
    #
    message = WSMessage[schemas.WSCommentUpdated](
        action=WSMessageAction.UpdatedComment,
        body=schemas.WSCommentUpdated(
            tweetId=comment.tweet_id,
            comment=return_comment
        )
    )
    await ws_manager.broadcast(message, current_user.id)

    return return_comment


@router.delete("", response_model=schemas.EmptyResponse)
async def delete_comment(
    request_body: schemas.CommentDelete,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):

    comment = crud.get_comment_by_id(db, request_body.commentId)
    # Broadcast a WS message so users can see the new comment get updated in real-time
    message = WSMessage[schemas.WSCommentDeleted](
        action=WSMessageAction.DeletedComment,
        body=schemas.WSCommentDeleted(
            tweetId=comment.tweet_id,
            commentId=request_body.commentId
        )
    )
    await ws_manager.broadcast(message, current_user.id)
    return crud.delete_comment(db, current_user.id, request_body)
