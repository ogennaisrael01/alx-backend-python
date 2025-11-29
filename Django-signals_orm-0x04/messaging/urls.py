from django.urls import path
from . import views


urlpatterns = [
    path("delete/account/<pk>/", views.delete_view, name="delete"),
    path("conversation/<conversation_pk>/message/<message_pk>/reply", views.message_reply, name="reply_to_message"),
    path("conversation/<conversation_pk>/message/<message_pk>/messages", views.nested_message_view, name="nested messages"),
    path("unread/messages/", views.unread_messages, name="unread-messages")
]
