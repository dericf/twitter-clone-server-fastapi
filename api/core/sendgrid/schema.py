from enum import Enum
import os

from pydantic import EmailStr


class EmailSender(EmailStr, Enum):
    ACCOUNT = os.environ.get("SEND_GRID_ACCOUNT_VERIFICATION_FROM_EMAIL")
    NOTIFICATIONS = os.environ.get("SEND_GRID_NOTIFICATIONS_FROM_EMAIL")
    PASSWORD_RECOVERY = os.environ.get(
        "SEND_GRID_PASSWORD_RECOVERY_FROM_EMAIL")
