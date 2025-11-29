from .utils.retry_on_failures import Log
from datetime import datetime, timedelta
from rest_framework.request import HttpRequest
import logging
from rest_framework.exceptions import PermissionDenied
from .models import CustomUser
from rest_framework import status

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
        restricted_paths = [
            '/api/v1/conversations/',
            '/api/v1/conversations/messages/'
        ]
  
        # if self.date > 7 or self.date < 17 and request.path in restricted_paths:
        #     raise PermissionDenied()
      
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware :
    def __init__(self, get_response):
        self.get_response = get_response
 
        self.max_message = 5 # total message allowed within the given time frame
        self.time_frame = 1 # time frame in minutes
        self.cache = {} # store each user request {ip_address: [timestamp, timestamp, .....]}


    def __call__(self, request: HttpRequest, *args, **kwds):
        ip_address = request.META.get("REMOTE_ADDR")
        current_date = datetime.now()
        if request.method == "POST":
            if not ip_address in self.cache:
                self.cache[ip_address] = {"time_frames": []}

            # clean out old time stamp outside time window
            clean_old_time_frames = current_date - timedelta(minutes=self.time_frame)
            # check how many message the user has sent in the last 60 seconds
            for ts in self.cache[ip_address]["time_frames"]:
                if ts > clean_old_time_frames:
                    message_count = len(self.cache[ip_address]["time_frames"])
                    if message_count >= self.max_message:
                        raise  PermissionDenied(
                            detail="Maximum alloed messages exceede: number of message allowed: {self.max_message}, message_sent: {message_Count}",
                            code=status.HTTP_403_FORBIDDEN)
            self.cache[ip_address]["time_frames"].append(current_date)
        response = self.get_response(request)
        print("query cache", self.cache)
        return response


class RolepermissionMiddleware:
    """ Restrict access to PUT PATCH and DELETE endpoints from guest users"""
    def __init__(self, get_response):
        self.get_response = get_response
        self.allwoed_roles = [CustomUser.RoleChoices.ADMIN, CustomUser.RoleChoices.HOST]

        self.admin_prvilages = ["PUT", "DELETE", "PATCH"]


    def check_role(self, request: HttpRequest):
        if hasattr(request.user, "is_superuser") and request.user.is_superuser:
            return True
        elif hasattr(request.user, "is_staff") and request.user.is_staff:
            return True
        elif request.user.role in self.allwoed_roles:
            return True
        else:
            return False

    def __call__(self, request: HttpRequest, *args, **kwds):
       
        if request.method in self.allwoed_roles and self.check_role(request) is False:
            raise PermissionDenied()
        
        response = self.get_response(request)
        return response





    

    
