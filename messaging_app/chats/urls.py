from django.urls import path, include
from rest_framework import routers
from .views import RegisterViews, ConversationViewSet, MessageViewSet
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename="conversation")

# Nested router connecting conversation to messages
conversation_router = routers.NestedDefaultRouter(router, r'conversations', lookup="conversation")
conversation_router.register(r'messages', MessageViewSet, basename="message")

urlpatterns = [
    path("register/", RegisterViews.as_view(), name="register"),
    path("", include(conversation_router.urls)),
    path('', include(router.urls)),

]