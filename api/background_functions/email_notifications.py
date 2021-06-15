# Standard Library
import os

# Core
from ..core.sendgrid import send_email, constants
from ..core.sendgrid.schema import EmailSender

# Models
from ..models import User, Comments

# SendGrid API
from sendgrid import SendGridAPIClient, Personalization, Asm
from sendgrid.helpers.mail import Mail

# TODO : implement function for:
#    - password recovery email


async def send_registration_confirmation_email(username: str, email: str, confirmation_key: str):
    #
    # Build Sendgrid Mail Object
    #
    message = Mail(from_email=EmailSender.ACCOUNT.value,
                   to_emails=email
                   )

    message.template_id = constants.REGISTRATION_CONFIRMATION_DYNAMIC_TEMPLATE_ID
    message.asm = Asm(
        constants.MAIN_UNSUBSCRIBE_GROUP_ID
    )
    message.dynamic_template_data = {
        "confirmation_url": f'{os.environ.get("PRODUCTION_CLIENT_HOST_URL")}/confirm-email?confirmationKey={confirmation_key}',
        "username": username
    }
    await send_email(message)


async def send_new_message_notification_email(user: User, other_user: User):
    #
    # Build Sendgrid Mail Object
    #
    message = Mail(from_email=EmailSender.NOTIFICATIONS.value,
                   to_emails=other_user.email
                   )

    notification_text = f"You have a new message from {user.username}! Please log in to view your messages."
    message.template_id = constants.NEW_NOTIFICATION_DYNAMIC_TEMPLATE_ID
    message.asm = Asm(
        constants.MAIN_UNSUBSCRIBE_GROUP_ID
    )
    message.dynamic_template_data = {
        "subject": "You have a new message",
        "username": other_user.username,
        "notification_text": notification_text,
        "log_in_url": f'{os.environ.get("PRODUCTION_CLIENT_HOST_URL")}/tweets'
    }
    await send_email(message)


async def send_new_comment_notification_email(tweet_owner: User, commenter: User, comment: Comments):
    #
    # Build Sendgrid Mail Object
    #
    message = Mail(from_email=EmailSender.NOTIFICATIONS.value,
                   to_emails=tweet_owner.email
                   )

    notification_text = f"{commenter.username} has commented \" {comment.content} \" on your tweet!"
    message.template_id = constants.NEW_NOTIFICATION_DYNAMIC_TEMPLATE_ID
    message.asm = Asm(
        constants.MAIN_UNSUBSCRIBE_GROUP_ID
    )
    message.dynamic_template_data = {
        "subject": f"A user commented on your tweet",
        "username": tweet_owner.username,
        "notification_text": notification_text,
        "log_in_url": f'{os.environ.get("PRODUCTION_CLIENT_HOST_URL")}/tweets'
    }
    await send_email(message)


async def send_new_follower_notification_email(user: User, new_follower: User):
    #
    # Build Sendgrid Mail Object
    #
    message = Mail(from_email=EmailSender.NOTIFICATIONS.value,
                   to_emails=user.email
                   )

    notification_text = f"{new_follower.username} started following you!"
    message.template_id = constants.NEW_NOTIFICATION_DYNAMIC_TEMPLATE_ID
    message.asm = Asm(
        constants.MAIN_UNSUBSCRIBE_GROUP_ID
    )
    message.dynamic_template_data = {
        "subject": f"You have a new follower",
        "username": user.username,
        "notification_text": notification_text,
        "log_in_url": f'{os.environ.get("PRODUCTION_CLIENT_HOST_URL")}/followers'
    }
    await send_email(message)
