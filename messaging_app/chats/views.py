from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Messages
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsOwnerOrReadOnly

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title", "created_at"]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]  # Ensure only authenticated users can access this view



class MessageViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["sent_by", "sent_at", "conversation"]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly] # Ensure only authenticated users can access this view