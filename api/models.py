from sqlalchemy import Boolean, Column, Integer, String, DateTime, Date,  ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, index=True)
    bio = Column(String, index=True)
    birthdate = Column(Date, index=True)
    hashed_password = Column(String, nullable=False)
    
    tweets = relationship("Tweet", back_populates="user", lazy="joined")
    followers = relationship("Follows", back_populates="user", foreign_keys="Follows.user_id", lazy="joined")
    follows = relationship("Follows", back_populates="follows_user", foreign_keys="Follows.follows_user_id", lazy="joined")
    comments = relationship("Comments", back_populates="user", lazy="joined")
    tweet_likes = relationship("TweetLikes", back_populates="user", lazy="joined")
    comment_likes = relationship("CommentLikes", back_populates="user", lazy="joined")


class Follows(Base):
    """<user_id> follows <follows_user_id>
    """
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    follows_user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="follows", foreign_keys=[user_id], lazy="joined")
    follows_user = relationship("User", back_populates="followers", foreign_keys=[follows_user_id], lazy="joined")


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tweets", foreign_keys=[user_id], lazy="joined")
    comments = relationship("Comments", back_populates="tweet", lazy="joined")
    likes = relationship("TweetLikes", back_populates="tweet", lazy="joined")


class TweetLikes(Base):
    __tablename__ = "tweet_likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tweet_id = Column(Integer, ForeignKey("tweets.id"))
    
    user = relationship("User", back_populates="tweet_likes", foreign_keys=[user_id], lazy="joined")
    tweet = relationship("Tweet", back_populates="likes", foreign_keys=[tweet_id], lazy="joined")



class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tweet_id = Column(Integer, ForeignKey("tweets.id"))
    content = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="comments", foreign_keys=[user_id], lazy="joined")
    tweet = relationship("Tweet", back_populates="comments", foreign_keys=[tweet_id], lazy="joined")
    likes = relationship("CommentLikes", back_populates="comment", foreign_keys="CommentLikes.comment_id", lazy="joined")


class CommentLikes(Base):
    __tablename__ = "comment_likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    comment_id = Column(Integer, ForeignKey("comments.id"))
    
    user = relationship("User", back_populates="comment_likes", foreign_keys=[user_id], lazy="joined")
    comment = relationship("Comments", back_populates="likes", foreign_keys=[comment_id], lazy="joined")

