from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import time
import os


# SQLALCHEMY_DATABASE_URL = "sqlite:///./twitter-clone.db"
SQLALCHEMY_DATABASE_URL = os.environ.get("POSTGRES_URL") # "postgresql://admin:secret@db:5432/twitterdb"

engine = None
SessionLocal = None
Base = None

retries = 5
while retries > 0:
    try:
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL #, connect_args={"check_same_thread": False}
        ) # remove connect_args for non-sqlite db
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base = declarative_base()
        break
    except Exception as e:
        print("Error connecting..." + str(e))
        retries -= 1
        time.sleep(3)
