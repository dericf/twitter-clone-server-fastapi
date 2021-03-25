# FastAPI
from fastapi import status, HTTPException

# SQLAlchemy
from sqlalchemy.orm import Session

# Types
from typing import Optional

# Custom Modules
from . import models, schemas
from .database import engine
from .core import security


def get_user_by_id(db: Session, user_id: int):
    """Get a single user by id
    """
    return db.query(models.User).filter(models.User.id == user_id).one_or_none()


def get_user_by_email(db: Session, email: str):
    """Get a single user by email
    """
    query = db.query(models.User).filter(models.User.email == email)
    # print(query.statement.compile(engine))
    return query.one_or_none()


def get_user_by_username(db: Session, username: str):
    """Get a single user by username
    """
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Get all users
    """
    query = db.query(models.User).offset(skip).limit(limit)
    # print(query.statement.compile(engine))
    return query.all()


def create_user(db: Session, user: schemas.UserCreate):
    """Add a user
    """
    db_user = models.User(
        email=user.email,
        username=user.username,
        bio=user.bio,
        birthdate=user.birthdate,
        hashed_password=security.get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate, skip: int = 0, limit: int = 100):
    user_db = db.query(models.User).filter(
        models.User.id == user_id).one_or_none()
    user_db.bio = user_update.bio
    db.commit()
    db.refresh(user_db)
    return user_db


def delete_user(db: Session, user_id: int):
    try:
        db.query(models.User).filter(models.User.id == user_id).delete()
        db.commit()
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")


##########
# TWEETS #
##########
def get_tweets(db: Session, skip: int = 0, limit: int = 100):
    result = db.query(models.Tweet).offset(skip).limit(limit).all()
    map(lambda r: print(dict(r)), result)
    return result


def get_tweets_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    # First check if user exists
    db_user = db.query(models.User).filter(models.User.id == user_id).one_or_none()
    
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")
    
    # user exists - proceed to return tweets
    return db_user.tweets


def create_user_tweet(db: Session, tweet: schemas.TweetCreate, user_id: int):
    db_tweet = models.Tweet(**tweet.dict())

    db_tweet.user_id = user_id

    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet


def update_tweet(db: Session, user_id: int, tweet_id: int, new_content: str):
    db_tweet: schemas.Tweet = db.query(models.Tweet).filter(
        models.Tweet.id == tweet_id).one_or_none()

    if not db_tweet:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="tweet not found")

    if db_tweet.user_id != user_id:
        # Tweet does not belong to the user. Cannot delete.
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="user does not own that tweet")

    db_tweet.content = new_content
    db.commit()
    db.refresh(db_tweet)
    return db_tweet


def delete_tweet(db: Session, user_id: int, tweet_id: int):
    db_tweet: schemas.Tweet = db.query(models.Tweet).filter(
        models.Tweet.id == tweet_id).one_or_none()
    if not db_tweet:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tweet not found")
    if db_tweet.user_id != user_id:
        # Tweet does not belong to the user
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to delete that tweet")
    try:
        db.delete(db_tweet)
        
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Something went wrong")


############
# COMMENTS #
############
def create_tweet_comment(db: Session, user_id: int, comment: schemas.CommentCreate):
    # First check that tweet exists
    db_tweet: schemas.Tweet = db.query(models.Tweet).filter(
        models.Tweet.id == comment.tweet_id).one_or_none()
    if not db_tweet:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tweet does not exist")
    
    # tweet exists - proceed to create comment
    db_comment = models.Comments(tweet_id=comment.tweet_id, user_id=user_id, content=comment.content)
    try:
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tweet does not exist")


def get_comments_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    db_user = db.query(models.User).filter(models.User.id == user_id).one_or_none()
    
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")
    return db_user.comments


def get_comments_for_tweet(db: Session, tweet_id: int, skip: int = 0, limit: int = 100):
    db_tweet = db.query(models.Tweet).filter(models.Tweet.id == tweet_id).one_or_none()
    
    if not db_tweet:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tweet does not exist")
    return db_tweet.comments


def update_comment(db: Session, user_id: int, comment: schemas.CommentUpdate):
    db_comment: schemas.Comment = db.query(models.Comments).filter(
        models.Comments.id == comment.comment_id).one_or_none()
    
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Comment does not exist")

    if db_comment.user_id != user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to update that comment")
    
    db_comment.content = comment.new_content
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, user_id: int, comment: schemas.CommentCreate):
    comment_db: schemas.Comment = db.query(models.Comments).filter(
        models.Comments.id == comment.comment_id).one_or_none()

    if not comment_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Comment does not exist")
    
    if comment_db.user_id != user_id:
        # comment does not belong to the user
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to delete that comment")
    
    try:
        db.delete(comment_db)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")
