#
# Utility functions for background tasks
#
async def send_registration_confirmation_email(email: str, confirmation_key: str):
    """Render the Email HTML (& PlainText) to a file
    """
    message: str = """ 
    This is a test
    """
    # with open("log.txt", mode="a") as email_file:
    #     content = f"notification for {email}: {message}"
    #     email_file.write(content)

    print(f'TESTING EMAIL CONFIRMATION')
    print(confirmation_key)
