from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..core import security
from ..core.config import settings
from ..dependencies import get_db

router = APIRouter(prefix="/tweets", tags=['tweets'])

@router.get("/", response_model=List[schemas.TweetResponse])
def get_all_tweets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
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


@router.post("/users/{user_id}/", response_model=schemas.Tweet)
def create_tweet_for_user(
    user_id: int, tweet: schemas.TweetCreate, db: Session = Depends(get_db)
):
    return crud.create_user_tweet(db=db, tweet=tweet, user_id=user_id)


@router.get("/user/{user_id}/", response_model=List[schemas.Tweet])
def get_tweets_for_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tweets = crud.get_tweets_for_user(db, user_id=user_id, skip=skip, limit=limit)
    return tweets

