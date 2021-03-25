# FastAPI
from fastapi import APIRouter, HTTPException, Request, Depends

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


@router.get("/{userId}", response_model=List[schemas.TweetResponse])
def get_tweets(userId: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    The GET method for this endpoint will send back either all, or specific 
    tweets based on user. This endpoint will always return an array of objects.

    If you want all tweets, simply make the GET request and send no data. If you
    want tweets from specific users, send the user Id

    --
    In the example, we send the numeric id 1. 
    The API returns tweets by user 1. 

    If you want all tweets, send no data.
    --

    An error will be returned if any userId does not exist.
    """
    if userId:
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


# @router.patch("/{tweetId}")
# def update_tweet(tweetId: int, tweet_body: schemas.TweetUpdate, db: Session = Depends(get_db)):
#     tweet = crud.update_tweet(
#         db, tweet=, skip=skip, limit=limit)
#     return
    


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
