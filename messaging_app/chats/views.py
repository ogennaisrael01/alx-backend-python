from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from .serializers import ResgisterSerializer, ConversationSerializer, MessageSerailizer, ConversationCreateSerailizer
from django.contrib.auth import get_user_model
from .models import Conversation, Messages, RoleChoices
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models  import Q

User = get_user_model()

class RegisterViewset(viewsets.ModelViewSet):
    permission_classes = []
    serializer_class = ResgisterSerializer
    queryset = User.objects.all()

    # continue code

class ConservationViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConversationCreateSerailizer
    queryset = Conversation.objects.prefetch_related("messages")
    lookup_field = "pk"

    def perform_create(self, serializer):
       """ Save the serialized data setting the current user as the user who created the conversation"""
       serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """"
            - Initiate a conversation 
            - Only HOST and ADMIN privilages are allowed

            send reqeust -
            ===== name - cnversation (must be included)
            ===== description - description 

            response - 
            ====  '{
                "name": "Library Members",
                "description": "Brief discussion about the library systems and related  manaagements"
            }

        """
        user = request.user

        if user.role not in [RoleChoices.ADMIN, RoleChoices.HOST]:
            msg = "Can't initiate converstaion"
            return Response(status=status.HTTP_403_FORBIDDEN, data= {"success": False, "message" : msg})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer=serializer)
        conversatioon = Conservation.objects.get(name=serializer.validated_data.get("name"))
        conservation.participants.add(user)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)
    

    def list(self, request, *args, **kwargs):
        """ Get all conversation where user is either host"""
        queryset = self.get_queryset()
        conversations = queryset.filter(user=request.user)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)
    
    @action(methods=["get"], detail=False, url_path='messages')
    def list_msg_with_converstaions(self, request, *args, **kwargs):
        # get all conversation where the current user is part or the participants
        user = request.user
        try:    
            queryset = self.get_queryset()
            conversations = queryset.filter(Q(user=user) | Q(participants=user)).prefetch_related("participants").distinct()
            if not conversations:
                return Response(status=status.HTTP_200_OK, data={"success": True, "message": "You are not in any conversation"}) 
            serializer = ConversationSerializer(conversations, many=True)
            return Response(status=status.HTTP_200_OK, data={"success": True, "data": serializer.data})
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"success": False, "message": e})