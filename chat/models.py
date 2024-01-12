from django.db import models
from accounts.models import UserAccount
from django.utils import timezone

# Create your models here.

class Chat(models.Model):
    sender = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='recieved_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender.username} - {self.receiver.username} - {self.timestamp}"

    class Meta:
        db_table = "chat"
        ordering = ("timestamp",)