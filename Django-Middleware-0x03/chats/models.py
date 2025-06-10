from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Custom user model extending Django's AbstractUser
class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField( max_length=64)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'  # Specify the field to use for authentication
    REQUIRED_FIELDS = ['email']  # Specify additional fields required for user creation
    
    @property
    def id(self):
        return self.user_id
    
    def __str__(self):
        return self.username
    

# Model representing a conversation between users
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")  # Users in the conversation
    title = models.TextField(default="start convasation")  # Optional title for the conversation
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation

    def __str__(self):
        return self.title

# Model representing a message in a conversation
class Messages(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)  # Link to conversation
    sent_by = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)  # User who sent the message
    message_body = models.TextField()  # Message content
    sent_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Message created by {self.sent_by} on {self.sent_at}. conversation = {self.conversation}"