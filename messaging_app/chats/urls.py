from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# Create a router and register our viewsets with it
router = routers.DefaultRouter()
router.register(r'conversation', ConversationViewSet)  # Routes for conversation endpoints
router.register(r'messages', MessageViewSet) # Routes for messages endpoints



urlpatterns = [
    path('', include(router.urls)),
]