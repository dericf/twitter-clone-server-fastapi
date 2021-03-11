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
    
    tweets = relationship("Tweet", back_populates="user")


class Tweet(Base):
    __tablename__ = "tweet"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tweets")