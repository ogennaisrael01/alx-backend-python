from .utils.retry_on_failures import Log
from datetime import datetime
from django.http import HttpRequest
import logging

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
        log_message = logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        # save every request log message in a file called request.log 
        with Log("request_log.log", "a") as file:
            file.write(f"{log_message} \n")

        response = self.get_response(request)
        return response

    
