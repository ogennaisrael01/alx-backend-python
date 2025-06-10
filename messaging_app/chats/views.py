from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Messages
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title", "created_at"]
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]  # Custom permission to check if user is a participant of the conversation



class MessageViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["sent_by", "sent_at", "conversation"]
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]  # Custom permission to check if user is a participant of the conversation

    # Override the perform_create method to set the sent_by field to the current user
    # This ensures that the user who sends the message is recorded correctly.
    def perform_create(self, serializer):
        serializer.save(sent_by=self.request.user)


    def get_queryset(self):
        queryset  = Messages.objects.all()
        conversation_id = self.request.query_params.get('conversation_id', None)

        if conversation_id is not None:
            queryset = Messages.objects.filter(conversation__conversation_id=conversation_id)
            # Check if the user is a participant of the conversation
                  
            conversation  = get_object_or_404(Conversation, conversation_id=conversation_id)
            if conversation.participants.filter(user_id=self.request.user.user_id).exists():
                return queryset
            else:
                # If the user is not a participant, return an empty queryset
                return Messages.objects.none()
        return queryset
