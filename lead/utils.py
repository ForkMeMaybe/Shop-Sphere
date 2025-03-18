from django.core.mail import send_mail
from django.conf import settings


def send_marketing_email(email, subject, message):
    """
    Sends a marketing email.

    Parameters:
    - email (str): Recipient email
    - subject (str): Email subject
    - message (str): Email body
    """
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # Ensure this is configured in settings.py
        [email],
        fail_silently=False,
    )
