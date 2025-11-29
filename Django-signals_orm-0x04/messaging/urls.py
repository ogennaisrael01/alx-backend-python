from django.urls import path
from . import views


urlpatterns = [
    path("delete/account/<pk>/", views.delete_view, name="delete"),
    path("conversation/<conversation_pk>/message/<message_pk>/reply", views.message_reply, name="reply_to_message")
]
