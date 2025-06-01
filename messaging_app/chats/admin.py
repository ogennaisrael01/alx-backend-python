from django.contrib import admin
from django.contrib import admin
from .models import User, Messages, Conversation


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ["username",  "phone_number", "date_joined"]

class MessageAdmin(admin.ModelAdmin):
    list_display = ['content', 'sender', 'date_created']

admin.site.register(User,  UserAdmin)
admin.site.register(Messages, MessageAdmin)
admin.site.register(Conversation)