# FastAPI
from fastapi import APIRouter, HTTPException, Request, Depends, status

# SQLAlchemy
from sqlalchemy.orm import Session

# Types
from typing import List, Optional

# Custom Modules
from .. import schemas, crud, models
from ..dependencies import get_db, get_current_user
from ..core import security
from ..core.config import settings
from ..core.websocket.connection_manager import ws_manager
from ..schemas.websockets import WSMessage, WSMessageAction

# FastAPI router object
router = APIRouter(prefix="/comment-likes", tags=['comment-likes'])


@router.get("", response_model=List[schemas.CommentLikeResponseBody])
def get_all_comment_likes(commentId: Optional[int] = None, db: Session = Depends(get_db)):
    """
    The GET method for this endpoint will send back either all, or specific likes based on comment. This endpoint will always return an array of objects.

    If you want all likes, simply make the GET request and send no data. If you want likes from a specific comment, send the comment Id

    In the example, we send the numeric id 1. The API returns all likes on comments 1. If you want all likes on all comments, send no data.

    An error will be returned if any commentId does not exist.
    """
    comment_likes: List[models.CommentLikes] = []
    if commentId:
        comment_likes = crud.get_all_comment_likes_for_comment(db, commentId)

    else:
        comment_likes = crud.get_all_comment_likes(db)

    return [
        schemas.CommentLikeResponseBody(
            commentLikeId=like.id,
            commentId=like.comment_id,
            userId=like.user.id,
            username=like.user.username
        ) for like in comment_likes
    ]


@router.post("", response_model=schemas.CommentLikeResponseBody)
async def like_a_comment(
    comment_body: schemas.CommentLikeCreateRequestBody,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    # validate & create the like record
    comment_like = crud.create_comment_like_for_comment(
        db=db, comment_id=comment_body.commentId, user_id=current_user.id)

    return_like = schemas.CommentLikeResponseBody(
        commentLikeId=comment_like.id,
        commentId=comment_like.comment_id,
        userId=comment_like.user.id,
        username=comment_like.user.username
    )

    message = WSMessage[schemas.WSCommentLikeUpdated](
        action=WSMessageAction.UpdatedCommentLike,
        body=schemas.WSCommentLikeUpdated(
            isLiked=True,
            commentLike=return_like
        )
    )
    await ws_manager.broadcast(message, current_user.id)

    return return_like


@router.delete("", response_model=schemas.EmptyResponse)
async def delete_comment_like(
        request_body: schemas.CommentLikeDeleteRequestBody,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)):

    comment_like = crud.get_comment_like_by_comment_id_and_user_id(
        db, current_user.id, request_body.commentId)

    delete_successful = crud.delete_comment_like_by_user_and_comment_id(
        db, current_user.id, request_body.commentId)

    message = WSMessage[schemas.WSCommentLikeUpdated](
        action=WSMessageAction.UpdatedCommentLike,
        body=schemas.WSCommentLikeUpdated(
            isLiked=False,
            commentLike=schemas.CommentLikeResponseBody(
                commentLikeId=comment_like.id,
                commentId=comment_like.comment_id,
                userId=comment_like.user.id,
                username=comment_like.user.username
            )
        )
    )
    await ws_manager.broadcast(message, current_user.id)

    # TODO return status for delete?
    return schemas.EmptyResponse()
