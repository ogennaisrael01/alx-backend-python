from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterViewset, ConservationViewset, MessageViewSet
from rest_framework_nested import routers


router = DefaultRouter()

router.register(r'register', RegisterViewset, basename="register")
router.register(r'conversations', ConservationViewset, basename="conversation")

# Nested router connecting conversation to messages
conversation_router = routers.NestedDefaultRouter(router, r'conversations', lookup="conversation")
conversation_router.register(r'messages', MessageViewSet, basename="message")

urlpatterns = [
    path("", include(conversation_router.urls)),
    path('', include(router.urls)),

]