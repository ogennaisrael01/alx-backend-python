from rest_framework import serializers
import email_validator
from django.contrib.auth.password_validation import validate_password as _validate_password
from django.contrib.auth import get_user_model
from .models import Conversation
from messaging.models import Message

User = get_user_model()

class ResgisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200)
    password = serializers.CharField( max_length=50, write_only=True)

    def validate_password(self, value):
        if value:
             return serializers.ValidationError("Please provide your password")
        _validate_password(value)
        return value
       
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
    

class Messageerailizer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source="sender.username")
    message_histories = serializers.SerializerMethodField()
    nested_messages = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = [
            'message_id', 
            "sender", 
            "message_body", 
            "sent_at",
            "edited",
            "message_histories",
            "nested_messages"
            ]

    def get_message_histories(self, obj):
        histories = obj.message_history.all()
        for history in histories[:1]:
            return {
                "current_message": history.message.message_body,
                "previous_message": history.message_body_history
            }
    def get_nested_messages(self, obj):
        nested_messages = obj.replies.all()
        return [
            {
                "sender": message.sender.username,
                "message": message.message_body
            }
            for message in nested_messages
        ]
    
class ConversationCreateSerailizer(serializers.Serializer):
    name = serializers.CharField(max_length=500, error_messages={
        "required": "This field is required",
        "blank": "This field cannot be blank",
        "max_length": "Name is too long"
    }
    )
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
    Message = Messageerailizer(many=True, read_only=True)
    participants_names = serializers.SerializerMethodField()
    last_msg = serializers.SerializerMethodField()
    class Meta:
        model = Conversation
        fields = [
            "conversation_id", 
            "name", 
            "description", 
            "user", 
            "participants", 
            "created_at", 
            "Message", 
            "participants_names", 
            "last_msg"
            ]

    def get_participants_names(self, obj):
        names = [name.username for name in obj.participants.all()]
        return names
    
    def get_last_msg(self, obj):
        last_msg = obj.message.first()
        if last_msg:
            return {""
                "sender": last_msg.sender.username,
                "message": last_msg.message_body
            }
        return None


class MessageCreate(serializers.Serializer):
    message_body = serializers.CharField(max_length=500, 
                                         error_messages={
                                    "required": "This field is required",
                                    "blank": "This field cannot be blank",
                                    "max_length": "Name is too long"
                                }
    )
 
    def validate_message_body(self, value: str):
        if len(value) < 2:
            raise serializers.ValidationError("message Body coan't be below two characters")
        return value

    def create(self, validated_data):
        message = Message.objects.create(**validated_data)
        return message
    
    def update(self, instance, validated_data):
        instance.message_body = validated_data.get("message_body", instance.message_body)
        instance.save()
        return instance
