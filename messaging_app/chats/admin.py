from django.contrib import admin
from django.contrib import admin
from .models import User, Messages, Conversation


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ["user_id", "email", "date_joined"]

class MessageAdmin(admin.ModelAdmin):
    list_display = ["message_id", 'sent_by', 'sent_at']

admin.site.register(User,  UserAdmin)
admin.site.register(Messages, MessageAdmin)
admin.site.register(Conversation)