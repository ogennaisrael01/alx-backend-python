from django.contrib import admin
from messaging.models import Message
from django.contrib.auth.models import User

# Register your admins here
admin.site.register(Message)
admin.site.register(User)