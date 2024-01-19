from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from carnova import settings
from user.models import Booking


@receiver(post_save, sender=Booking)
def send_email_on_save(sender, instance, **kwargs):
    subject = "Booking Detail"
    message = (
        f"Dear {instance.user.user.username},\n\n"
        f"We are excited to inform you that your booking has been confirmed!\n"
        f"Booking Details:\n"
        f"Order Number: {instance.order_number}\n"
        f"Car: {instance.car}\n"
        f"Pickup Date: {instance.pickup_date}\n"
        f"Return Date: {instance.return_date}\n"
        f"Total Amount: {instance.total_amount}\n\n"
        f"Thank you for choosing our car rental service. We hope you have a great experience!\n\n"
        f"Best regards,\n"
        f"The Carnova Team"
    )

    to_email = instance.user.user.email

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )
