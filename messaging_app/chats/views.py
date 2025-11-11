from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ResgisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterViewset(viewsets.ModelViewSet):
    permission_classes = []
    serializer_class = ResgisterSerializer
    queryset = User.objects.all()

    
