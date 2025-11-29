from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import uuid

class CustomeUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
            - Create and Save user credentials in the database
            - create and save user using email and password, raise validations error if not provided
        """
        if not email:
            raise ValueError("Please enter your email adderess")
        if not password:
            raise ValueError("Please enter your password")
 
        normalized_email = self.normalize_email(email)
        user = self.model(email=normalized_email, password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """  
            - Create and return a super user with admin privilages
            - is_superuser =True
            - is_staff =True
        """
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("A staff user must have is_staff field set to True")
        if not extra_fields.get("is_superuser"):
            raise ValueError("A super user  must have the is_superuser field set to True")
        user = self.create_user(email=email, password=password, **extra_fields)

        return user
    


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class RoleChoices(models.TextChoices):
        GUEST = 'GUEST', 'guest'
        ADMIN = 'ADMIN', 'admin'
        HOST = 'HOST', 'host'
    class RegistrationMethod(models.TextChoices):
        EMAIL = "EMAIL", "email"
        GOOGLE = "GOOGLE", "google"

    id = models.UUIDField(
        max_length=20, 
        primary_key=True,
        default=uuid.uuid4
        )
    email =  models.EmailField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    role = models.CharField(max_length=20, choices=RoleChoices.choices, default=RoleChoices.HOST)
    phone_number = models.CharField(max_length=25, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username =  models.CharField(max_length=200, unique=True, null=True, blank=True)
    registration_method = models.CharField(max_length=20, choices=RegistrationMethod.choices, default=RegistrationMethod.EMAIL)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomeUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]
        verbose_name = 'Custom users'
        indexes = [
            models.Index(fields=["email"], name="email_idx"),
            models.Index(fields=["role"], name="role_idx"),
            models.Index(fields=["id"], name="id_idx"),
            models.Index(fields=["-created_at"], name="created_desc_idx"),
            models.Index(fields=["username"], name="username_idx"),
            models.Index(fields=["registration_method"], name="register_idx")
        ]

    @property
    def is_admin(self) -> bool:
        return self.is_superuser
    
    @property
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return None
    
    def __str__(self) -> str:
        return f"{self.email} ==== {self.role}"



class Conversation(models.Model):
    conversation_id = models.UUIDField(
        max_length=20,
        primary_key=True,
        default=uuid.uuid4,
        db_index=True)
    name = models.CharField(
        max_length=500, 
        null=False, 
        blank=False)

    description = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name="owned_conversations", null=True)
    participants = models.ManyToManyField(CustomUser, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "conversations"
        verbose_name = "Conversations"
    def __str__(self):
        return f"{self.user.username} == Created by === {self.name}"


class Messages(models.Model):
    message_id = models.UUIDField(
        max_length=20, 
        primary_key=True,
        default=uuid.uuid4,
        db_index=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "messages"
        verbose_name = "Messages"
        ordering = ["-created_at"]
    
    def __str__(self):
        return  f"{self.sender.username} ==== {self.message_body}"