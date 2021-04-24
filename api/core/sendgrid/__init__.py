from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

from typing import Union, List


def send_email(to_emails: Union[List[str], str], subject: str, html_content: str):
    #
    # Build Sendgrid Mail Object
    #
    message = Mail(from_email=os.environ.get("SEND_GRID_FROM_EMAIL"),
                   to_emails=to_emails,
                   subject=subject,
                   html_content=html_content)

    try:
        sg = SendGridAPIClient(os.environ.get("SEND_GRID_API_KEY"))
        response = sg.send(message)

    except Exception as e:
        print("error")
