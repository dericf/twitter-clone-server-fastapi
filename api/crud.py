# FastAPI
from fastapi import status, HTTPException

# SQLAlchemy
from sqlalchemy.orm import Session
from sqlalchemy import or_

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


def get_user_by_email_or_username(db: Session, email: str):
    """Get a single user by email or by uername
    """
    query = db.query(models.User).filter(
        or_(models.User.email == email, models.User.username == email))
    # print(query.statement.compile(engine))
    return query.first()


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


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdateRequestBody):
    user_db = db.query(models.User).filter(
        models.User.id == user_id).one_or_none()
    if user_update.newBio:
        user_db.bio = user_update.newBio
    if user_update.newUsername:
        user_db.username = user_update.newUsername
    db.commit()
    db.refresh(user_db)
    return user_db


def delete_user(db: Session, user_id: int):
    try:
        db.query(models.User).filter(models.User.id == user_id).delete()
        db.commit()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")


##########
# TWEETS #
##########
def get_tweet_by_id(db: Session, tweet_id: int):
    return db.query(models.Tweet).filter(models.Tweet.id == tweet_id).one_or_none()


def get_tweets(db: Session, skip: int = 0, limit: int = 100):
    print("GETTING TWEETS")
    return db.query(models.Tweet).order_by(models.Tweet.created_at.desc()).offset(skip).limit(5).all()


def get_tweets_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    # First check if user exists
    print("GETTING TWEETS FOR USER")
    db_user = db.query(models.User).filter(
        models.User.id == user_id).one_or_none()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")

    # user exists - proceed to return tweets
    tweets = db.query(models.Tweet).filter(models.Tweet.user_id == user_id).order_by(
        models.Tweet.created_at.desc()).limit(limit).all()
    return tweets


def get_tweets_liked_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    # First check if user exists
    print("GETTING TWEETS FOR USER")
    db_user = db.query(models.User).filter(
        models.User.id == user_id).one_or_none()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")

    # user exists - proceed to return tweets
    tweets = [tweet_like.tweet for tweet_like in db_user.tweet_likes]
    return tweets


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
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="tweet not found")

    if db_tweet.user_id != user_id:
        # Tweet does not belong to the user. Cannot delete.
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="user does not own that tweet")

    db_tweet.content = new_content
    db.commit()
    db.refresh(db_tweet)
    return db_tweet


def delete_tweet(db: Session, user_id: int, tweet_id: int):
    db_tweet: schemas.Tweet = db.query(models.Tweet).filter(
        models.Tweet.id == tweet_id).one_or_none()
    if not db_tweet:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Tweet not found")
    if db_tweet.user_id != user_id:
        # Tweet does not belong to the user
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authorized to delete that tweet")
    try:
        db.delete(db_tweet)
        db.commit()

    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail="Something went wrong")


############
# COMMENTS #
############
def create_tweet_comment(db: Session, user_id: int, comment: schemas.CommentCreate):
    # First check that tweet exists
    db_tweet: schemas.Tweet = db.query(models.Tweet).filter(
        models.Tweet.id == comment.tweetId).one_or_none()
    if not db_tweet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Tweet does not exist")

    # tweet exists - proceed to create comment
    db_comment = models.Comments(
        tweet_id=comment.tweetId, user_id=user_id, content=comment.content)
    try:
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Tweet does not exist")


def get_comment_by_id(db: Session, comment_id: int):
    db_comment = db.query(models.Comments).filter(
        models.Comments.id == comment_id).one_or_none()
    return db_comment


def get_comments_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    # Check the user exists first
    db_user = db.query(models.User).filter(
        models.User.id == user_id).one_or_none()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")

    # User exists - proceed to return comments
    return db_user.comments


def get_comments_for_tweet(db: Session, tweet_id: int, skip: int = 0, limit: int = 100):
    db_tweet = db.query(models.Tweet).filter(
        models.Tweet.id == tweet_id).one_or_none()

    if not db_tweet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Tweet does not exist")
    return db_tweet.comments


def update_comment(db: Session, user_id: int, comment: schemas.CommentUpdate):
    db_comment: schemas.Comment = db.query(models.Comments).filter(
        models.Comments.id == comment.commentId).one_or_none()

    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Comment does not exist")

    if db_comment.user_id != user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authorized to update that comment")

    db_comment.content = comment.newContent
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, user_id: int, comment: schemas.CommentCreate):
    comment_db: schemas.Comment = db.query(models.Comments).filter(
        models.Comments.id == comment.commentId).one_or_none()

    if not comment_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Comment does not exist")

    if comment_db.user_id != user_id:
        # comment does not belong to the user
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authorized to delete that comment")

    try:
        db.delete(comment_db)
        db.commit()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")

#############
# FOLLOWS #
#############


def get_all_users_following(db: Session, user_id: int):
    db_followers = db.query(models.Follows).filter(
        models.Follows.user_id == user_id).all()
    print("DB Following: ", db_followers)
    return db_followers


def create_follow_relationship(db: Session, user_id: int, follow_user_id: int):
    # First check if the user id is valid
    check_user = db.query(models.User).filter(
        models.User.id == follow_user_id).one_or_none()

    if not check_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Bad userId. User does not exist")

    # User exists - proceed to check if user already follows follow_user_id

    existing_follow = db.query(models.Follows).filter(
        models.Follows.user_id == user_id, models.Follows.follows_user_id == follow_user_id).one_or_none()

    if existing_follow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Already following user.")

    # User exists & does not already follow - proceed to create follow relationship/link
    db_follows = models.Follows(
        user_id=user_id, follows_user_id=follow_user_id)
    db.add(db_follows)
    db.commit()
    db.refresh(db_follows)
    return db_follows


def delete_follow_relationship(db: Session, user_id: int, follow_user_id: int):
    # First check if the user id is valid
    check_user = db.query(models.User).filter(
        models.User.id == user_id).one_or_none()

    if not check_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Bad userId. User does not exist")

    # User exists - proceed to check if follow relationship/link exists

    existing_follow = db.query(models.Follows).filter(
        models.Follows.user_id == user_id, models.Follows.follows_user_id == follow_user_id).one_or_none()

    if not existing_follow:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Cannot un-follow user that is not being followed")

    # Follow relationship exists - proceed to un-follow
    db.delete(existing_follow)
    db.commit()
    return

#############
# FOLLOWERS #
#############


def get_all_followers(db: Session, user_id: int):
    # Check if user_id is valid
    existing_user = db.query(models.User.id).filter(
        models.User.id == user_id).one_or_none()

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Bad userId. User does not exist.")

    # User is valid - proceed to get all followers
    db_followers = db.query(models.Follows).filter(
        models.Follows.follows_user_id == user_id).all()
    print("DB Followers: ", db_followers)
    return db_followers

###############
# Tweet Likes #
###############


def get_tweet_like_by_id(db: Session, tweet_like_id: int):
    """Get a single tweet_like object/row
    """
    return db.query(models.TweetLikes).filter(models.TweetLikes.id == tweet_like_id).one_or_none()


def get_all_tweet_likes(db: Session):
    return db.query(models.TweetLikes).limit(2).all()


def get_all_tweet_likes_for_tweet(db: Session, tweet_id: int):
    # First check if tweet exists
    print("Getting tweet likes!")
    existing_tweet = get_tweet_by_id(db, tweet_id)
    if not existing_tweet:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail="Error. Tweet does not exist")

    db_tweet_likes = db.query(models.TweetLikes).filter(
        models.TweetLikes.tweet_id == tweet_id).limit(2).all()

    # user exists - proceed to return tweets
    return db_tweet_likes


def create_tweet_like_for_tweet(db: Session, tweet_id: int, user_id: int):
    """Add a tweet like for tweet && user
    """
    #! TODO: first check if user has already like this tweet
    db_tweet_like = models.TweetLikes(
        user_id=user_id,
        tweet_id=tweet_id
    )
    db.add(db_tweet_like)
    db.commit()
    db.refresh(db_tweet_like)
    return db_tweet_like


def delete_tweet_like(db: Session, user_id: int, tweet_id: int,):
    """Delete (Unlike) a tweet
    """
    db_tweet_like = db.query(models.TweetLikes).filter(
        models.TweetLikes.tweet_id == tweet_id).first()

    if not db_tweet_like:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail="Error. Cannot Delete. Bad ID for Like")

    # First check if tweet like and user match
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail="Error. User does not exist.")

    if db_user.id != db_tweet_like.user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized to unike this tweet.")

    # Data is valid - proceed to delete tweet like (un-like)
    db.delete(db_tweet_like)
    db.commit()
    return


# --------------------

###############
# Comment Likes #
###############

def get_comment_like_by_id(db: Session, comment_like_id: int):
    """Get a single comment_like object/row
    """
    return db.query(models.CommentLikes).filter(models.CommentLikes.id == comment_like_id).one_or_none()


def get_all_comment_likes(db: Session):
    return db.query(models.CommentLikes).all()


def get_all_comment_likes_for_comment(db: Session, comment_id: int):
    # First check if comment exists

    existing_comment = get_comment_by_id(db, comment_id)
    if not existing_comment:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail="Error. Comment does not exist")

    db_comment_likes = db.query(models.CommentLikes).filter(
        models.CommentLikes.comment_id == comment_id).all()

    # user exists - proceed to return comments
    return db_comment_likes


def create_comment_like_for_comment(db: Session, comment_id: int, user_id: int):
    """Add a comment like for comment && user
    """
    # Check if the comment exists
    existing_comment = get_comment_by_id(db, comment_id)
    if not existing_comment:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail="Error. Comment does not exist")

    # Check if comment like already exists
    db_comment_like = db.query(models.CommentLikes).filter(
        models.CommentLikes.comment_id == comment_id, models.CommentLikes.user_id == user_id).first()

    if db_comment_like:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail="Error. Already liked comment.")

    db_comment_like = models.CommentLikes(
        user_id=user_id,
        comment_id=comment_id
    )

    db.add(db_comment_like)
    db.commit()
    db.refresh(db_comment_like)
    return db_comment_like


def delete_comment_like(db: Session, user_id: int, comment_like_id: int,):
    """Delete (Unlike) a comment
    """
    db_comment_like = db.query(models.CommentLikes).filter(
        models.CommentLikes.id == comment_like_id).one_or_none()

    if not db_comment_like:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail="Error. Cannot Delete. Bad ID for Like")

    # First check if comment like and user match
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail="Error. User does not exist.")

    if db_user.id != db_comment_like.user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized.")

    # Data is valid - proceed to delete comment like (un-like)
    db.delete(db_comment_like)
    db.commit()
    return
