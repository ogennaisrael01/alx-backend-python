from django.db import models
import uuid
from django.contrib.auth import get_user_model
from chats.models import Message

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
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="nofification_message")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications_sender")
    receiver = models.ManyToManyField(User, related_name="notification_receivers")

    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = "notifications"
        verbose_name = "conversation"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Nootiication('{self.notification_id}, {self.sender.username}, {self.reciever.username}, {self.is_read}, {self.timestamp})"
    

class MessageHistory(models.Model):
    message_history_id = models.UUIDField(
        max_length=20,
        primary_key=True,
        default=uuid.uuid4,
        db_index=True
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="message_history")
    message_body_history = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"MesssageHistory('{self.edited_by}, {self.edited_at}')"
    
    class Meta:
        ordering = ["-edited_at"]