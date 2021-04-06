from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import time
import os


def get_db_connection_url():
    env = os.environ.get("ENV")
    print(env)
    print(os.environ.get("LOCAL_DOCKER_INTERNAL_POSTGRES_URL"))
    if not env:
        return ""

    if env == "development":
        return os.environ.get("LOCAL_DOCKER_INTERNAL_POSTGRES_URL")

    elif env == "staging":
        return os.environ.get("STAGING_POSTGRES_URL")

    elif env == "production":
        return os.environ.get("PRODUCTION_POSTGRES_URL")


SQLALCHEMY_DATABASE_URL = get_db_connection_url()

engine = None
SessionLocal = None
Base = None

retries = 5
while retries > 0:
    try:
        engine = create_engine(
            # , connect_args={"check_same_thread": False}
            SQLALCHEMY_DATABASE_URL
        )  # remove connect_args for non-sqlite db
        SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=engine)
        Base = declarative_base()
        print("DB Connected")
        break
    except Exception as e:
        print("Error connecting..." + str(e))
        retries -= 1
        time.sleep(3)
