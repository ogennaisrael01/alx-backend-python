from .utils.retry_on_failures import Log
from datetime import datetime, timedelta
from rest_framework.request import HttpRequest
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

# class RestrictAccessByTimeMiddleware:
#     """" Restrict Access to chat from time outside 6pm to 9pm"""
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.date = datetime.now().hour

#     def __call__(self, request: HttpRequest, *args, **kwds):
#         """ Restrict access the these urls
#             - [
#             '/api/v1/conversations/,
#             'api/v1/conversations/messages/'
#         ]
#         """
#         restricted_path = [
#             '/api/v1/conversations/',
#             '/api/v1/conversations/messages/'
#         ]
#         if request.path in restricted_path:
#             raise PermissionDenied()
#         if request and self.date > 21 or self.date < 18:
#             raise PermissionDenied()
      
#         response = self.get_response(request)
#         return response


class OffensiveLanguageMiddleware :
    def __init__(self, get_response):
        self.get_response = get_response
 
        self.max_message = 5 # total message allowed within the given time frame
        self.time_frame = 60 # time frame in seconds
        self.cache = {} # store each user request {ip_address: [timestamp, timestamp, .....]}


    def __call__(self, request: HttpRequest, *args, **kwds):
        ip_address = request.META.get("REMOTE_ADDR")
        current_date = datetime.now()
        if request.method == "POST":
            if ip_address in self.cache.keys():
                # check how many message the user has sent in the last 60 seconds
                last_message = self.cache[ip_address]["time_frames"][-1]
                message_count = len(self.cache[ip_address]["time_frames"])

                total_minutes  = last_message - timedelta(minutes=1)
                if total_minutes.second >= self.time_frame and message_count >= self.max_message:
                    raise PermissionDenied()
                
            self.cache.update({
                ip_address: {
                    "time_frames": [],
                }
            })
            self.cache[ip_address]["time_frames"].append(current_date)
        response = self.get_response(request)
        return response





    

    
