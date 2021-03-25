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


@router.get("/", response_model=List[schemas.TweetResponse])
def get_all_tweets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """The GET method for this endpoint will send back all tweets     
    """
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


@router.get("/{userId}", response_model=List[schemas.TweetResponse])
def get_tweets(userId: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    The GET method for this endpoint will send back specific 
    tweets based on user.

    An error will be returned if any userId does not exist.
    """

    tweets = crud.get_tweets_for_user(db, userId, skip=skip, limit=limit)

    if not tweets:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="User does not exist")

    return [
        schemas.TweetResponse(
            tweetId=tweet.id,
            content=tweet.content,
            createdAt=tweet.created_at,
            userId=tweet.user.id,
            username=tweet.user.username
        ) for tweet in tweets
    ]


@router.post("/", response_model=schemas.TweetResponse)
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


@router.put('/{tweet_id}', response_model=schemas.EmptyResponse)
def update_tweet(
        tweet_id: int,
        request_body: schemas.TweetUpdate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)):
    update_successful = crud.update_tweet(db, current_user.id, tweet_id, request_body.newContent)
    
    return {}


@router.delete('/{tweet_id}', response_model=schemas.EmptyResponse)
def delete_tweet(tweet_id: int,
                 db: Session = Depends(get_db),
                 current_user: schemas.User = Depends(get_current_user)):
    delete_successful = crud.delete_tweet(db, current_user.id, tweet_id)
    
    return {}
