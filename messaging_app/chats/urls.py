from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterViewset, ConservationViewset


routers = DefaultRouter()

routers.register(r'register', RegisterViewset, basename="register")
routers.register(r'conversation', ConservationViewset, basename="conversation")
urlpatterns = [
    path('', include(routers.urls)),

]