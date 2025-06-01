from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user model extending Django's AbstractUser
class User(AbstractUser):
    phone_number = models.CharField(max_length=15)  # Extra field for user's phone number

    def __str__(self):
        return self.username

# Model representing a conversation between users
class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations")  # Users in the conversation
    title = models.TextField(default="")  # Optional title for the conversation
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation

    def __str__(self):
        return self.title

# Model representing a message in a conversation
class Messages(models.Model):
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)  # Link to conversation
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)  # User who sent the message
    content = models.TextField()  # Message content
    date_created = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Message created by {self.sender} on {self.date_created}. conversation = {self.conversation}"