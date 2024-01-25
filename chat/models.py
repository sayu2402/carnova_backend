from django.db import models
from accounts.models import UserAccount
from django.utils import timezone
from user.models import *

# Create your models here.


class Chat(models.Model):
    sender = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="recieved_messages"
    )
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, default=None, null=True, blank=True
    )

    def __str__(self):
        return f"{self.sender.username} - {self.receiver.username} - {self.timestamp}"

    class Meta:
        db_table = "chat"
        ordering = ("timestamp",)


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("car_approved", "Car Approved"),
        ("car_rejected", "Car Rejected"),
    ]

    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.notification_type}: {self.message}"
