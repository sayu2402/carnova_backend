from celery import shared_task
from django.core.mail import send_mail
from datetime import datetime
from accounts.models import *
from carnova import settings


@shared_task
def send_morning_emails():
    users = UserAccount.objects.filter(role="user")
    # Send email to each user
    for user in users:
        subject = "Good morning! Check out our latest offers."
        message = (
            "Good morning! Here are the latest updates from our car rental service."
        )
        to_mail = user.email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_mail],
            fail_silently=True,
        )

    return "Done"
