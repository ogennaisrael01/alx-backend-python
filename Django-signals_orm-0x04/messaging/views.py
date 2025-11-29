
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.http import HttpRequest
from chats.models import Message, Conversation
from chats.serializers import MessageCreate

User = get_user_model()

@api_view(http_method_names=["DELETE"])
def delete_view(request: HttpRequest, pk) -> Response:
    if not pk:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, msg={"success": False, "msg": "ID is required"})

    user = get_object_or_404(User, pk=pk)
    if request.user.email != user.email:
        return Response(status=status.HTTP_403_FORBIDDEN, data="You can't perform this action")
    delete_user = user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=["POST"])
def message_reply(request: HttpRequest, message_pk, conversation_pk) -> Response:
    if request.method != "POST":
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data="Method is not allowed")
    serializer = MessageCreate(data=request.data)
    serializer.is_valid(raise_exception=True)
    message = get_object_or_404(Message, pk=message_pk)
    conversation = get_object_or_404(Conversation, pk=conversation_pk)
    serializer.save(parent_message=message, sender=request.user, conversation=conversation)
    return Response(serializer.validated_data)
