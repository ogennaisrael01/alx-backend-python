from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Custom user model extending Django's AbstractUser
class CustomUser(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username
    

# Model representing a conversation between users
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(CustomUser, related_name="conversations")  # Users in the conversation
    title = models.TextField(default="")  # Optional title for the conversation
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation

    def __str__(self):
        return self.title

# Model representing a message in a conversation
class Messages(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)  # Link to conversation
    sent_by = models.ForeignKey(CustomUser, related_name="sender", on_delete=models.CASCADE)  # User who sent the message
    message_body = models.TextField()  # Message content
    sent_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Message created by {self.sent_by} on {self.sent_at}. conversation = {self.conversation}"