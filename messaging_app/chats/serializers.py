from rest_framework import serializers
from .models import User, Conversation, Messages
from rest_framework.serializers import ValidationError, SerializerMethodField

# Serializer for the custom User model
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, max_length=15)
    class Meta:
        model = User
        fields = ["username", "date_joined", "email", "password"]

    def validate_password(self, value):
        if not value:
            raise ValidationError("Enter your password")
        return value

# Serializer for the Messages model
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ["message_id", "conversation", "message_body", "sent_by"]

# Serializer for the Conversation model, includes nested messages
class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)  # Nested messages in the conversation
    class Meta:
        model = Conversation
        fields = ["conversation_id", "title", "participants", "created_at", "messages"]