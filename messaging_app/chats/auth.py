from rest_framework_simplejwt import serializers
from rest_framework_simplejwt import views
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from .utils.retry_on_failures import retry_on_failures
from django.conf import settings



class CustomTokenSerializer(serializers.TokenObtainPairSerializer):
    def get_token(self, user):
        token = super().get_token(user=user)
        
        token["username"] = user.username
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name

        return token


class CustomTokenView(views.TokenObtainPairView):
    serializer_class = CustomTokenSerializer


def google_auth(token):
    try:       
        payload = retry_on_failures(id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            "407408718192.apps.googleusercontent.com"

        ))   
    except (Exception, ValueError) as e:
        return {"success": False, "msg": f"Error: {e}"}
    return {"success": True, "data": payload}