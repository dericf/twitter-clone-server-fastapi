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
router = APIRouter(prefix="/tweets", tags=['tweets'])


@router.get("", response_model=List[schemas.TweetResponse])
def get_all_tweets(userId: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """The GET method for this endpoint will send back all tweets     
    """
    if userId:
        user = crud.get_user_by_id(db, userId)
        if not user:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                detail="Error.Bad userId. User does not exist.")
        tweets = crud.get_tweets_for_user(db, userId, skip=skip, limit=limit)
    else:
        tweets = crud.get_tweets(db, skip=skip, limit=limit)
    return [
        schemas.TweetResponse(
            tweetId=tweet.id,
            content=tweet.content,
            createdAt=tweet.created_at,
            userId=tweet.user.id,
            username=tweet.user.username
        ) for tweet in tweets
    ]


@router.get("/liked", response_model=List[schemas.TweetResponse])
def get_all_tweets_liked_by_user(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)):
    """Return all tweets liked by the authenticated user
    """

    tweets = crud.get_tweets_liked_by_user(
        db, current_user.id, skip=skip, limit=limit)

    return [
        schemas.TweetResponse(
            tweetId=tweet.id,
            content=tweet.content,
            createdAt=tweet.created_at,
            userId=tweet.user.id,
            username=tweet.user.username
        ) for tweet in tweets
    ]


@router.get("/one/{tweetId}", response_model=schemas.TweetResponse)
def get_single_tweet_by_id(
    tweetId: int,
    db: Session = Depends(get_db)
):
    """Return a single tweet based on a tweetId
    """

    tweet = crud.get_tweet_by_id(db, tweetId)

    return schemas.TweetResponse(
        tweetId=tweet.id,
        content=tweet.content,
        createdAt=tweet.created_at,
        userId=tweet.user.id,
        username=tweet.user.username
    )


@router.post("", response_model=schemas.TweetResponse)
def create_tweet_for_user(tweet_body: schemas.TweetCreate,
                          db: Session = Depends(get_db),
                          current_user: schemas.User = Depends(get_current_user)):
    tweet = crud.create_user_tweet(
        db=db, tweet=tweet_body, user_id=current_user.id)
    return schemas.TweetResponse(
        tweetId=tweet.id,
        content=tweet.content,
        createdAt=tweet.created_at,
        userId=tweet.user.id,
        username=tweet.user.username
    )


@router.put('/{tweetId}', response_model=schemas.EmptyResponse)
def update_tweet(
        tweetId: int,
        request_body: schemas.TweetUpdate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)):
    update_successful = crud.update_tweet(
        db, current_user.id, tweetId, request_body.newContent)

    return {}


@router.delete('/{tweetId}', response_model=schemas.EmptyResponse)
def delete_tweet(tweetId: int,
                 db: Session = Depends(get_db),
                 current_user: schemas.User = Depends(get_current_user)):
    delete_successful = crud.delete_tweet(db, current_user.id, tweetId)

    return {}
