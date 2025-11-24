from .utils.retry_on_failures import Log
from datetime import datetime
from django.http import HttpRequest
import logging
from rest_framework.exceptions import PermissionDenied

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """"
        - Middleware for logging each user request to a file, including timestamp and other related infomation
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest, *args, **kwds):
        now = datetime.now().strftime("%d-%B-%Y %H:%M:%S")
        user = request.user
        log_message = f"{now} - User: {user} - Path: {request.path}"

        # save every request log message in a file called request.log 
        with Log("requests.log", "a") as file:
            file.write(f"{log_message} \n")

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    """" Restrict Access to chat from time outside 6pm to 9pm"""
    def __init__(self, get_response):
        self.get_response = get_response
        self.date = datetime.now().hour

    def __call__(self, request: HttpRequest, *args, **kwds):
        """ Restrict access the these urls
            - [
            '/api/v1/conversations/,
            'api/v1/conversations/messages/'
        ]
        """
        restricted_path = [
            '/api/v1/conversations/',
            '/api/v1/conversations/messages/'
        ]
        if request.path in restricted_path:
            raise PermissionDenied()
        if request and self.date > 21 or self.date < 18:
            raise PermissionDenied()
      
        response = self.get_response(request)
        return response



    

    
