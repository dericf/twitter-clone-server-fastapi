from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .core.config import get_db_connection_url

import time
import os

engine = None
SessionLocal = None
Base = None

retries = 5
while retries > 0:
    try:
        engine = create_engine(
            get_db_connection_url()
        )
        SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=engine)
        Base = declarative_base()
        print("DB Connected")
        break
    except Exception as e:
        print("Error connecting..." + str(e))
        retries -= 1
        time.sleep(3)
