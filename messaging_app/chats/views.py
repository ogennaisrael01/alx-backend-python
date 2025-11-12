
from rest_framework import viewsets, permissions, status
from .serializers import (
    ResgisterSerializer, 
    ConversationSerializer,
    MessageSerailizer, 
    ConversationCreateSerailizer,
    MessageCreate,
)

from django.contrib.auth import get_user_model
from .models import Conversation, Messages, RoleChoices
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models  import Q
from django.utils import timezone

User = get_user_model()

class RegisterViewset(viewsets.ModelViewSet):
    permission_classes = []
    serializer_class = ResgisterSerializer
    queryset = User.objects.all()

    # continue code

class ConversationViewSet(viewsets.ModelViewSet):
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
        conversatioon = Conversation.objects.filter(name=serializer.validated_data.get("name"), user=user).first()
        conversatioon.participants.add(user)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)
    

    def list(self, request, *args, **kwargs):
        """ Get all conversation where current user is the  host"""
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

        
    @action(methods=["post"], detail=False, url_path="add-user")
    def add_user_to_conservation(self, request, *args, **kwargs):
        """
            - Add users to conversations 
            - user_is = query_params
            - conversation_id = query_params
        """
        user_id = request.query_params.get("user_id")
        conversation_id = request.query_params.get("conversation_id")
        msg = ""  
        if not user_id:
            msg += "Please provide the user id of the person you want to include to your conversation"
            return Response(msg)
        if not conversation_id:
            msg += "please provide the conversation id"
            return Response(msg)
     
        user_obj = get_object_or_404(User, id=user_id)
        conversation_obj = get_object_or_404(Conversation, conversation_id=conversation_id)
        try:
            if request.user.id != conversation_obj.user.id:
                return Response(status=status.HTTP_403_FORBIDDEN, data={"message": "Can't perform this action"})
            if user_obj in conversation_obj.participants.all():
                return Response(status=status.HTTP_302_FOUND, data={"success": f'{user_obj.username} is already in {conversation_obj.name}'})
            conversation_obj.participants.add(user_obj)    
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"success": False, "message": f"Unable to add {user_obj.username} to {conversation_obj.name}: {e}"})
        return Response(status=status.HTTP_200_OK, data={
            "success": True,
            "message": f"add {user_obj.username} to {conversation_obj.name}"
        })

    @action(methods=["post"], detail=False, url_path="remove-user")
    def remove_user_from_conversation(self, request, *args, **kwargs):
        """"
            - Remove user from your conversations
        """
        user_id = request.query_params.get("user_id")
        conversation_id = request.query_params.get("conversation_id")
        strp_conversation_id = conversation_id.strip()
        strp_user_id = user_id.strip()
        msg = ''
        if not user_id:
            msg += "provide the user id"
            return Response(msg)
        if not conversation_id:
            msg += "provide conversation id"
            return Response(msg)

        user_obj = get_object_or_404(User, id=strp_user_id)
        conversation_obj = get_object_or_404(Conversation, conversation_id=strp_conversation_id)
        try:
            if request.user != conversation_obj.user:
                msg += "Can't perform this action"
                return Response(status_code=status.HTTP_403_FORBIDDEN, data=msg)
            if user_obj not in conversation_obj.participants.all():
                msg += f"{user_obj.user} is not in your conversation"
                return Response(status=status.HTTP_400_BAD_REQUEST, data=msg)
            conversation_obj.participants.remove(user_obj)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "success": False,
                "message": f"Error: {e}"
            }) 
        
        return Response(status=status.HTTP_200_OK, data={
            "success": True, 
            "message": f"You removed {user_obj.username}"
        })
    
    def update(self, request, *args, **kwargs):
        conversation_id = kwargs.get("pk")
        strp_conversation_id = conversation_id.strip()
        conversation_obj = get_object_or_404(Conversation, conversation_id=strp_conversation_id)
        if request.user.id != conversation_obj.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN, data={
                "success": False,
                "message": "You cant perform this action"
            })
        serializer = self.get_serializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            Conversation.objects.filter(conversation_id=conversation_id).update(updated_at=timezone.now(), **serializer.validated_data)
            return Response(status=status.HTTP_200_OK, data={
                "success": True,
                "message": "updated successfull",
                "data": serializer.validated_data
            }
            )
    def retrieve(self, request, *args, **kwargs):
        conversation_id = kwargs.get("pk")
        strp_conversation_id = conversation_id.strip()
        conversation = get_object_or_404(Conversation, conversation_id=strp_conversation_id, user=request.user)
        print(conversation)
        serializer = ConversationSerializer(conversation)
        return Response(status=status.HTTP_200_OK, data={
            "success": True,
            "data": serializer.data
            }
            )

    def destroy(self, request, *args, **kwargs):
        conversation_id = kwargs.get("pk")
        strp_conversation_id = conversation_id.strip()
        conversation_obj = get_object_or_404(Conversation, conversation_id=strp_conversation_id)
        if conversation_obj.user == request.user:
            conversation_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN, data="Can't perform this action")

    
class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageCreate
    queryset = Messages.objects.all()
    lookup_field = 'pk'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation_id = kwargs.get("conversation_pk") 
        strp_conversation_id = conversation_id.strip()
        msg = ''
        if not strp_conversation_id:
            msg += "please provide the conversation id"
            return Response(status=status.HTTP_400_BAD_REQUEST, data=msg)
        try:
            conversation_obj = get_object_or_404(Conversation, conversation_id=strp_conversation_id)
            # check is the user is in list o fparticipants

            if request.user not in conversation_obj.participants.all():
                msg +=  "You can't contribute to this conversation"
                return Response(status=status.HTTP_403_FORBIDDEN, data={"success": False, "message": msg})
        except Exception as e:
            msg += str(e)
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"success": False, "message": f"Error: {msg}"})

        serializer.save(sender=request.user, conversation=conversation_obj)
        msg += "message sent"
        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "success": True,
                'message': msg,
                "message_body": serializer.validated_data 
            }
        )

