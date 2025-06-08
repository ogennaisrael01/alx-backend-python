from rest_framework import permissions
class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    All CRUD operations (GET, POST, PUT, DELETE, PATCH) are allowed for participants.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        return  request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the object.
        return obj.owner == request.user