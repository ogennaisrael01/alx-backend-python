from rest_framework import permissions
from .models import Conversation, Messages


class IsPaticipantsOfConversation(permissions.BasePermission):
    """ A custom permission to check for user in a conversation or actually is the host of that conversation """

    def has_permission(self, request, view):
        return request.user.is_authenticated
    

    def has_object_permission(self, request, view, obj): 
        # if obj is convesation
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()   
        # if the obj is from the message class
        elif isinstance(obj, Messages):
            return request.user in obj.conversation.participants.all()
        
        return False
