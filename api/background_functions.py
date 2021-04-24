import os

from .core.sendgrid import send_email
#
# Utility functions for background tasks
#


async def send_registration_confirmation_email(email: str, confirmation_key: str):
    """Render the Email HTML (& PlainText) to a file
    """
    confirm_link = f'{os.environ.get("PRODUCTION_CLIENT_HOST_URL")}/confirm-email?confirmationKey={confirmation_key}'
    html_content = f"""
    Copy this link in your browser to confirm your email: <br /> <br />
    <b>{confirm_link}</b>
    <br />
    <br />
    <br />
    <br />
    
    Thanks, <br />
    ----------------------- <br />
    twitter-clone | programmertutor.com
    """
    subject = "Please Confirm Your Account"
    send_email(to_emails=email,
               subject=subject, html_content=html_content)
