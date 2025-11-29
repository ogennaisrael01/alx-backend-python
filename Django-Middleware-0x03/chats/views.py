
from rest_framework import viewsets, permissions, status, generics
from .serializers import (
    ResgisterSerializer, 
    ConversationSerializer,
    Messageerailizer, 
    ConversationCreateSerailizer,
    MessageCreate,
)

from django.contrib.auth import get_user_model
from .models import Conversation, Message
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models  import Q
from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework.views import APIView
from .auth import google_auth
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsPaticipantsOfConversation
from .pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend

User = get_user_model()

class EmailAuthApi(generics.CreateAPIView):
    permission_classes = []
    serializer_class = ResgisterSerializer
    queryset = User.objects.all()

    # continue code

class GoogleAuthApi(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get("id_token")

        if not token:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"msg": "provide your google token"})  
        payload = google_auth(token)
        if payload.get("success") is not True:
            return Response(data=payload.get("msg"))
        data = payload.get("data")

        email = data.get("email")
        name = data.get("name")
        profile_picture = data.get("profile_picture")
        try:
            user, created = User.objects.get_or_create(email=email)
            if created:
                user.set_unusable_password()
                user.email = email
                user.username = email.split("@")[0]
                user.first_name = name.split(" ")[0]
                user.last_name = name.split(" ")[1]
                user.registration_method = CustomUser.RegistrationMethod.GOOGLE
                user.save()
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"msg": "Plaase register with google"})

        refresh = RefreshToken.for_user(user)
        return Response(status=status.HTTP_201_CREATED, 
                        data={
                            "success": True,
                            "msg": "User created via google",
                            "token": {
                                "access": str(refresh.access_token),
                                "refresh": str(refresh)
                            },
                            "user_data": {
                                "email": user.email,
                                "username": user.username
                            }
                        })

class ConversationViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated, IsPaticipantsOfConversation]
    permission_classes = []
    serializer_class = ConversationCreateSerailizer
    queryset = Conversation.objects.prefetch_related("Message", "participants")
    lookup_field = "pk"
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields  = ["name", "user__username", "Message__message_body", "created_at"]

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

        if user.role not in [CustomUser.RoleChoices.ADMIN, CustomUser.RoleChoices.HOST]:
            msg = "you can't initiate a converstaion"
            return Response(status=status.HTTP_403_FORBIDDEN, data= {"success": False, "message" : msg})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer=serializer)
        conversatioon = Conversation.objects.filter(name=serializer.validated_data.get("name"), user=user).first()
        conversatioon.participants.add(user)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)
    

    def list(self, request, *args, **kwargs):
        """ Get all conversation where current user is the  host"""
        queryset = self.get_queryset().select_related("user")
        conversations = queryset.filter(user=request.user)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)
    
    @action(methods=["get"], detail=False, url_path='Message')
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
    permission_classes = [permissions.IsAuthenticated, IsPaticipantsOfConversation]
    serializer_class = MessageCreate
    queryset = Message.objects.all()
    lookup_field = 'pk'
    pagination_class = [CustomPagination]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["sender__username",  "message_body", "convesation__name"]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation_id = kwargs.get("conversation_pk") 
        strp_conversation_id = conversation_id.strip()
        msg = ''
        if not conversation_id:
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


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        conversation_id = kwargs.get("conversation_pk")
        msg = ''
        if not conversation_id:
            msg += "please provide your conversation id"
            return Response(status=status.HTTP_400_BAD_REQUEST, data=msg)
        strp_conversation_id = conversation_id.strip()
        try:
            conversation_obj = get_object_or_404(Conversation, conversation_id=strp_conversation_id)
            if request.user in conversation_obj.participants.all():
                queryset = conversation_obj.Message.all()
            
                serializer = Messageerailizer(queryset, many=True)
                return  Response(status=status.HTTP_200_OK, data={"success": True, "result": serializer.data})
        except Exception as e:
            msg += f"error occured: {str(e)}"
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"success": False, "msg": msg})
        
    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        conversation_id = kwargs.get("conversation_pk").strip()
        message_id = kwargs.get("pk").strip()
        try:
            conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
            message = queryset.filter(conversation=conversation, message_id=message_id)
        except Exception as e:
            msg = f"Error occured: {e}"
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"success": False, "msg": msg})
        serializer = Messageerailizer(message, many=True)
        return Response(status=status.HTTP_200_OK, data={"success": True, "data": serializer.data})


    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        conversation_id = kwargs.get("conversation_pk").strip() 
        queryset = self.get_queryset()
        message_id = kwargs.get("pk").strip()
        try:
            conversation_obj = get_object_or_404(Conversation, conversation_id=conversation_id)
            message_upt = queryset.filter(
                conversation=conversation_obj, 
                message_id=message_id, 
                sender=request.user).update(**serializer.validated_data)
            
            if message_upt == 1:
                return Response(status=status.HTTP_200_OK, data={"success": True, "msg": "updated message"})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={"success": False, "msg": "error updating message"})
        
        except Exception as e:
            msg = f'error occurred: {e}'
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"success": False, "msg": msg})


    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        conversation_id = kwargs.get("conversation_pk").strip()
        message_id = kwargs.get("pk").strip()
        try:
            message = queryset.filter(message_id=message_id).first()
            conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
            if message.sender == request.user or request.user.role in [CustomUser.RoleChoices.ADMIN, CustomUser.RoleChoices.HOST]:
                # delete the message is the user meets the requirements
                queryset.filter(conversation=conversation, message_id=message_id).delete()

                return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            msg = f"Error occurred: {e}"
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"success": False, "msg": msg})
        