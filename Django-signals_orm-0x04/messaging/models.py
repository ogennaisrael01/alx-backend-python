from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()
class Notification(models.Model):
    notification_id = models.UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid.uuid4,
        null=False,
        max_length=20
    )
    content = models.TextField()

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications_sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_reciever")

    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = "notifications"
        verbose_name = "conversation"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Nootiication('{self.notification_id}, {self.sender.username}, {self.reciever.username}, {self.is_read}, {self.timestamp})"