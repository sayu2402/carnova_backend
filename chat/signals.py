from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserAccount, Notification
import json
from vendor.models import CarHandling

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=UserAccount)
def send_onlineStatus(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        user = instance.id
        user_status = instance.online_status

        data = {"id": user, "status": user_status}

        async_to_sync(channel_layer.group_send)(
            "user", {"type": "send_onlineStatus", "value": json.dumps(data)}
        )


@receiver(post_save, sender=CarHandling)
def car_status_notification(sender, instance, created, **kwargs):
    if instance.verification_status == 'Approved':
        message = f"Your car ({instance.brand} {instance.car_name}) has been approved by the admin."
        notification_type = 'car_approved'
    elif instance.verification_status == 'Rejected':
        message = f"Your car ({instance.brand} {instance.car_name}) has been rejected by the admin."
        notification_type = 'car_rejected'
    else:
        return

    Notification.objects.create(
        message=message,
        notification_type=notification_type
    )

    # Send notification to the vendor group
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'vendor_notifications',
        {
            "type": "send_notification",
            "notification_type": notification_type,
            "message": message
        }
    )
