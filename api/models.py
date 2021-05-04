from sqlalchemy import Boolean, Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
# from sqlalchemy.dialects.postgresql import JSONB

from .database import Base


class User(Base):
    """
    TODO: Need to sort relationships by date - most recent first
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, index=True)
    bio = Column(String, index=True)
    birthdate = Column(Date, index=True)
    hashed_password = Column(String, nullable=False)
    confirmation_key = Column(String, nullable=True)
    account_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    tweets = relationship("Tweet", back_populates="user")
    followers = relationship(
        "Follows", back_populates="user", foreign_keys="Follows.user_id")
    follows = relationship(
        "Follows", back_populates="follows_user", foreign_keys="Follows.follows_user_id")
    comments = relationship("Comments", back_populates="user")
    tweet_likes = relationship("TweetLikes", back_populates="user")
    comment_likes = relationship("CommentLikes", back_populates="user")

    inbox = relationship("Messages", back_populates="user_from",
                         foreign_keys="Messages.user_from_id")
    outbox = relationship("Messages", back_populates="user_to",
                          foreign_keys="Messages.user_to_id")

    def __repr__(self):
        return f"{self.id} | {self.username}"


class Follows(Base):
    """<user_id> follows <follows_user_id>
    """
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    follows_user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="follows",
                        foreign_keys=[user_id])
    follows_user = relationship(
        "User", back_populates="followers", foreign_keys=[follows_user_id])


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tweets",
                        foreign_keys=[user_id])
    comments = relationship("Comments", back_populates="tweet")
    likes = relationship("TweetLikes", back_populates="tweet")


class TweetLikes(Base):
    __tablename__ = "tweet_likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tweet_id = Column(Integer, ForeignKey("tweets.id"))

    user = relationship("User", back_populates="tweet_likes",
                        foreign_keys=[user_id])
    tweet = relationship("Tweet", back_populates="likes",
                         foreign_keys=[tweet_id])


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tweet_id = Column(Integer, ForeignKey("tweets.id"))
    content = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="comments",
                        foreign_keys=[user_id])
    tweet = relationship("Tweet", back_populates="comments",
                         foreign_keys=[tweet_id])
    likes = relationship("CommentLikes", back_populates="comment",
                         foreign_keys="CommentLikes.comment_id")


class CommentLikes(Base):
    __tablename__ = "comment_likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    comment_id = Column(Integer, ForeignKey("comments.id"))

    user = relationship(
        "User", back_populates="comment_likes", foreign_keys=[user_id])
    comment = relationship(
        "Comments", back_populates="likes", foreign_keys=[comment_id])


class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_from_id = Column(Integer, ForeignKey("users.id"))
    user_to_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user_from = relationship(
        "User", back_populates="inbox", foreign_keys=[user_from_id])

    user_to = relationship(
        "User", back_populates="outbox", foreign_keys=[user_to_id])
