from django.shortcuts import render
from rest_framework import viewsets
from .models import Conversation, Messages
from .serializers import ConversationSerializer, MessageSerializer

# ViewSet for CRUD operations on Conversation model
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

# ViewSet for CRUD operations on Messages model
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer