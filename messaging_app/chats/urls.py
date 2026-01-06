from django.urls import path, include
from rest_framework import routers
from .views import EmailAuthApi, ConversationViewSet, MessageViewSet, GoogleAuthApi
from rest_framework_nested import routers
from .auth import CustomTokenView


router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename="conversation")

# Nested router connecting conversation to Message
conversation_router = routers.NestedDefaultRouter(router, r'conversations', lookup="conversation")
conversation_router.register(r'Message', MessageViewSet, basename="message")

urlpatterns = [
    path("register/", EmailAuthApi.as_view(), name="register"),
    path("token/obtain/", CustomTokenView.as_view(), name="token-obtain"),
    path("google/auth/", GoogleAuthApi.as_view(), name="google-auth"),
    path("", include(conversation_router.urls)),
    path('', include(router.urls)),

]
n