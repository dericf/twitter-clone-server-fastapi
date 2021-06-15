# FastAPI
from fastapi import APIRouter, HTTPException, Request, Depends, status, BackgroundTasks

# SQLAlchemy
from sqlalchemy.orm import Session

# Types
from typing import List, Optional

# Custom Modules
from .. import schemas, crud
from ..dependencies import get_db, get_current_user
from ..background_functions.email_notifications import send_new_follower_notification_email
from ..core import security
from ..core.config import settings

from ..core.websocket.connection_manager import ws_manager


# FastAPI router object
router = APIRouter(prefix="/follows", tags=['follows'])


@router.get("/{userId}", response_model=List[schemas.FollowsResponse])
def get_follows(userId: int, db: Session = Depends(get_db)):
    """
    The GET method for this endpoint requires a userId and will send 
    back information about all users the userId follows . 

    Returns:
    This endpoint will always return an array of objects.

    Errors:
    An error will be returned if the userId does not exist.
    """

    user = crud.get_user_by_id(db, userId)

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="User does not exist")

    follows = crud.get_all_users_following(db, userId)
    return [
        schemas.FollowsResponse(
            userId=following.follows_user.id,
            email=following.follows_user.email,
            username=following.follows_user.username,
            bio=following.follows_user.bio,
            birthdate=following.follows_user.birthdate
        ) for following in follows
    ]


@router.get("/count/{userId}", response_model=schemas.CountBase)
def get_follows_count_for_user(
    userId: int,
    db: Session = Depends(get_db)
):
    count = crud.get_following_for_user(db, user_id=userId)

    return schemas.CountBase(
        count=count
    )


@router.post("", response_model=schemas.EmptyResponse)
async def create_follow_record_for_user(
    request_body: schemas.FollowsCreateRequestBody,
    bg_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """
    The POST method for this endpoint will create a follow relationship between two users.

    current_user requests to follow a new user

    """
    crud.create_follow_relationship(
        db, current_user.id, request_body.followUserId)

    #
    # Broadcast WS message so user components can update
    #
    message = schemas.WSMessage[schemas.WSFollowsUpdateBody](
        action=schemas.WSMessageAction.NewFollower,
        body=schemas.WSFollowsUpdateBody(
            userId=current_user.id,
            followUserId=request_body.followUserId
        )
    )

    if not ws_manager.user_is_online(request_body.followUserId):
        # Send a notification email
        new_follower = crud.get_user_by_id(db, request_body.followUserId)
        bg_tasks.add_task(send_new_follower_notification_email,
                          new_follower, current_user)

    await ws_manager.broadcast(message, current_user.id)

    return schemas.EmptyResponse()


@router.delete('', response_model=schemas.EmptyResponse)
async def delete_follow_relationship(
    request_body: schemas.FollowsDeleteRequestBody,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    delete_successful = crud.delete_follow_relationship(
        db, current_user.id, request_body.followUserId)

    #
    # Broadcast WS message so user components can update
    #
    message = schemas.WSMessage[schemas.WSFollowsUpdateBody](
        action=schemas.WSMessageAction.LostFollower,
        body=schemas.WSFollowsUpdateBody(
            userId=current_user.id,
            followUserId=request_body.followUserId
        )
    )
    await ws_manager.broadcast(message, current_user.id)

    return schemas.EmptyResponse()
