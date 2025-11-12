from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterViewset, ConservationViewset


router = DefaultRouter()

router.register(r'register', RegisterViewset, basename="register")
router.register(r'conversation', ConservationViewset, basename="conversation")
urlpatterns = [
    path('', include(router.urls)),

]