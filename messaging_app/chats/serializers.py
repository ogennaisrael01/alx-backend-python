from rest_framework import serializers
import email_validator
from django.contrib.auth.password_validation import validate_password as _validate_password
from django.contrib.auth import get_user_model
from .models import Conversation, Messages

User = get_user_model()

class ResgisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200)
    password = serializers.CharField(
        max_length=50,
        write_only=True,
        required=True,
        error_messages={
            "blank": "password cannot be blank",
            "required": "password is required for registration"
        }
    )
    role = serializers.ChoiceField(choices=["HOST", 'ADMIN', 'GUEST'])

    def validate_password(self, value):
        if value:
            password = _validate_password(value)
            return password
        return serializers.ValidationError("Please provide your password")
    
    def validate_email(self, value: str):
        email = value.lower()

        try:
            valid_email = email_validator.validate_email(email, check_deliverability=True)
        except email_validator.EmailNotValidError as e:
            raise serializers.ValidationError(f"can't validate your email address: {e}")
        if  User.objects.filter(email=valid_email, is_active=True).exists():
            raise serializers.ValidationError("User woth this email already exists")
        return valid_email.normalized
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class MessageSerailizer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source="sender.username")
    class Meta:
        model = Messages
        fields = ['message_id', "sender", "message", "created_at"]

    
class ConversationCreateSerailizer(serializers.Serializer):
    name = serializers.CharField(max_length=500, error_messages={
        "blank": "conversation name connaot be blank",
        "required": "name is required"
    })
    description = serializers.CharField(max_length=1000)

    def validate(self, attrs):
        if len(attrs["name"]) < 2 :
            msg = "Conversation name connot be less than two  characters"
            raise serializers.ValidationError(msg)

        if len(attrs["description"]) > 1000: 
            msg = "Exceeded maximaum characters"
            raise serializers.ValidationError(msg)

        return attrs

    def create(self, validated_data):
        conversation = Conversation.objects.create(**validated_data)
        return conversation
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance
    

class ConversationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    messages = MessageSerailizer(many=True, read_only=True)
    participants_names = serializers.SerializerMethodField()
    last_msg = serializers.SerializerMethodField()
    class Meta:
        model = Conversation
        fields = ["name", "description", "user", "participants", "created_at", "messages", "participants_names", "last_msg"]

    def get_participants_names(self, obj):
        names = [name.username for name in obj.participants.all()]
        return names
    
    def get_last_msg(self, obj):
        last_msg = obj.messages.first()
        if last_msg:
            return {""
                "sender": last_msg.sender.username,
                "message": last_msg.message
            }
        return None
