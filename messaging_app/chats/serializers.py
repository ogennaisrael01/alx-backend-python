from rest_framework import serializers
import email_validator
from django.contrib.auth.password_validation import validate_password as _validate_password
from django.contrib.auth import get_user_model

User = get_user_model()

class ResgisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200)
    password = serializers.CharField(
        max_lenth=50,
        write_only=True,
        required=True,
        error_messages={
            "blank": "password cannot be blank",
            "required": "password is required for registration"
        }
    )

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
    
