from django.db import models
from django.contrib.auth.models import User
import uuid

# Register your models here

class Message(models.Model):
    messaging_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messaging') 
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciever')    
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when the message is created

    def __str__(self):
        return f"Message from {self.sender.username} to {self.reciever.username} at {self.timestamp}: {self.message}"

class Notification(models.Model):
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')  # User who receives the notification
    notification = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications')  # Link to the message that triggered the notification
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when the notification is created

    def __str__(self):
        return f"Notification for {self.user.username} at {self.timestamp}"