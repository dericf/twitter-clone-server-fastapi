# SQLAlchemy
from sqlalchemy.orm import Session

# Types
from typing import Optional

# Custom Modules
from . import models, schemas
from .database import engine
from .core import security


def get_user(db: Session, user_id: int):
    """Get a single user by id
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


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


def delete_user(db: Session, user_id: int, user: schemas.UserUpdate):
    try:
        db.query(models.User).filter(models.User.id == user.id).delete()
        db.commit()
        return True
    except Exception as e:
        return False


def get_tweets(db: Session, skip: int = 0, limit: int = 100):
    result = db.query(models.Tweet).offset(skip).limit(limit).all()
    map(lambda r: print(dict(r)), result)
    return result


def get_tweets_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Tweet).filter(models.Tweet.user_id == user_id).offset(skip).limit(limit).all()


def create_user_tweet(db: Session, tweet: schemas.TweetCreate, user_id: int):
    db_tweet = models.Tweet(**tweet.dict())

    db_tweet.user_id = user_id

    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet


def update_tweet(db: Session, user_id: int, tweet: schemas.TweetUpdate):
    db_tweet: schemas.Tweet = db.query(models.Tweet).filter(
        models.Tweet.id == tweet.id).one_or_none()

    if db_tweet.user_id != user_id:
        # TODO Raise exception here
        return None

    db_tweet.content = tweet.newContent
    db.commit()
    db.refresh(db_tweet)
    return db_tweet


def delete_tweet(db: Session, user_id: int, tweet_id: int):
    tweet_db: schemas.Tweet = db.query(models.Tweet).filter(
        models.Tweet.id == tweet_id).one_or_none()
    if tweet_db.user_id != user_id:
        # Tweet does not belong to the user
        return False
    try:
        db.delete(tweet_db)
        return True
    except Exception as e:
        return False


def create_tweet_comment(db: Session, user_id: int, comment: schemas.CommentCreate):
    db_comment = models.Comments(**comment.dict())
    db_comment.user_id = user_id
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Comments).filter(models.Comments.user_id == user_id).offset(skip).limit(limit).all()


def get_comments_for_tweet(db: Session, tweet_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Comments).filter(models.Comments.tweet_id == tweet_id).offset(skip).limit(limit).all()


def update_comment(db: Session, comment: schemas.CommentUpdate):
    db_comment = db.query(models.Comments).filter(
        models.Comments.id == comment.id).one_or_none()
    db_comment.content = comment.new_content
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, user_id: int, comment_id: int):
    comment_db: schemas.Comment = db.query(models.Comments).filter(
        models.Comments.id == comment_id).one_or_none()
    if comment_db.user_id != user_id:
        # comment does not belong to the user
        return False
    try:
        db.delete(comment_db)
        return True
    except Exception as e:
        return False
