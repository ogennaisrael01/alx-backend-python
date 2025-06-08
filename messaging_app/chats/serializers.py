from rest_framework import serializers
from .models import User, Conversation, Messages
from rest_framework.serializers import ValidationError, SerializerMethodField

# Serializer for the custom User model
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, max_length=15)
    class Meta:
        model = User
        fields = ["username", "date_joined", "email", "password"]

    def validate_password(self, obj):
        if not obj.password:
            raise ValidationError("Enter your password")
        return obj.password

# Serializer for the Messages model
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Messages
        fields = ["message_id", "conversation", "message_body", "sender"]
        read_only_fields = ["message_id", "sent_at"]  # Make message_id and sent_at read-only

    def validate_message_body(self, obj):
        if not obj:
            raise ValidationError("Message body cannot be empty")
        return obj
    
# Serializer for the Conversation model, includes nested messages
class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True) # Nested messages in the conversation
    participants = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = ["conversation_id", "title", "participants", "created_at", "messages"]

    def validate_title(self, obj):
        if not obj:
            raise ValidationError("Conversation title cannot be empty")
        return obj
    def validate_participants(self, obj):
        if not obj:
            raise ValidationError("Participants cannot be empty")
        return obj