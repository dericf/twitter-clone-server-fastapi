#
# Utility functions for background tasks
#
def write_notification(email: str, message=""):
    """Render the Email HTML (& PlainText) to a file
    """
    with open("log.txt", mode="a") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)