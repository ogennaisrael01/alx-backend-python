from rest_framework import serializers
from .models import User, Conversation, Messages

# Serializer for the custom User model
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password should not be readable
    class Meta:
        model = User
        fields = ["id", "username", "date_joined", "email", "password"]

# Serializer for the Messages model
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ["id", "conversation", "content", "date_created", "sender"]

# Serializer for the Conversation model, includes nested messages
class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)  # Nested messages in the conversation

    class Meta:
        model = Conversation
        fields = ["id", "title", "participants", "created_at", "messages"]