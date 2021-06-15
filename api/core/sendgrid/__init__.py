# Standard Library
import os
from typing import Union, List
from enum import Enum

from pydantic import EmailStr


# SendGrid API
from sendgrid import SendGridAPIClient, Personalization, Asm
from sendgrid.helpers.mail import Mail

# Utilities
from .schema import EmailSender
from ... import models


async def send_email(message: Mail):
    try:
        sg = SendGridAPIClient(os.environ.get("SEND_GRID_API_KEY"))
        response = sg.send(message)

    except Exception as e:
        print("error sending email", e)
