# Standard Library
import os

# Types
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = str(os.environ.get("SECRET_KEY"))
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # SERVER_NAME: str
    # SERVER_HOST: AnyHttpUrl

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "Twitter Clone Project"

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT", "")
            and values.get("EMAILS_FROM_EMAIL", "")
        )

    EMAIL_TEST_USER: EmailStr = os.environ.get(
        "EMAIL_TEST_USER")  # type: ignore
    FIRST_SUPERUSER: EmailStr = os.environ.get("FIRST_SUPERUSER_EMAIL")
    FIRST_SUPERUSER_PASSWORD: str = os.environ.get("FIRST_SUPERUSER_PASSWORD")
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True


settings = Settings()


def get_db_connection_url():
    env = os.environ.get("ENV")
    if not env:
        return ""

    if env == "localhost-development":
        return os.environ.get("LOCAL_POSTGRES_URL")

    elif env == "development":
        return os.environ.get("LOCAL_DOCKER_INTERNAL_POSTGRES_URL")

    elif env == "staging":
        return os.environ.get("STAGING_POSTGRES_URL")

    elif env == "production":
        return os.environ.get("PRODUCTION_POSTGRES_URL")
