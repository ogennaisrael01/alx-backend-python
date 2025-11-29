from rest_framework import permissions
from .models import Conversation, Messages


class IsPaticipantsOfConversation(permissions.BasePermission):
    """ A custom permission to check for user in a conversation"""

    def has_permission(self, request, view):
        return request.user.is_authenticated
    

    def has_object_permission(self, request, view, obj): 
        if not request.user.is_authenticated:
            return False
        if isinstance(obj, Messages):
            if request.user in obj.conversation.participants.all():
                return request.method in ["PUT", "PATCH", "DELETE", "GET"]
        
        return False
