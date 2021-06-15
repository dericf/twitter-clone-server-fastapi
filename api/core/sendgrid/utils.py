# Standard Library
import os
import http.client

# SendGrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Content

# Beautiful Soup
from bs4 import BeautifulSoup


def get_text_from_html(html):
    soup = BeautifulSoup(html)
    plain_text = soup.get_text()
    return Content("text/plain", plain_text)
