from datetime import datetime, timedelta

class RequestLoggingMiddleware:
    """
    A middleware that logs each user’s requests to a file, including the timestamp, user and the request path
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        time = datetime.now()
        user = request.user if request.user.is_authenticated else 'Anonymous'  
        path = request.path
        log_entry = f"{time} - {user} - {path}\n"

        # Log the request to a file
        with open("request.log", "a") as log_file:
            log_file.write(log_entry)

        return self.get_response(request)
    
class RestrictAccessByTimeMiddleware:
    """
    A middleware that restricts access to the messaging up during certain hours of the day
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__ (self, request):
        time = datetime.now().hour
        # Restrict access from 9 PM to 6 Am
        if time >= 21 and time <= 6:
            print(f"Cant access chat from from  9pm to 6am", status=404)

        return self.get_response(request)

class OffensiveLanguageMiddleware:
    """
    A middleware that limits the number of chat messages a user can send within a certain time window, based on their IP address.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_count = {}

    def __call__(self, request):
        user_ip = request.META.get('REMOTE_ADDR')
        current_time = datetime.now()

        # Initialize the message count for the user if not already present
        if user_ip not in self.message_count:
            self.message_count[user_ip] = {'count': 0, 'last_reset': current_time}

        # Reset the count if more than 1 minute has passed
        if current_time - self.message_count[user_ip]['last_reset'] > timedelta(minutes=1):
            self.message_count[user_ip] = {'count': 0, 'last_reset': current_time}

        # Increment the count for the current user
        self.message_count[user_ip]['count'] += 1

        # Check if the user has exceeded the limit of 5 messages in the last minute
        if self.message_count[user_ip]['count'] > 5:
            return (f"Too many messages from {user_ip}. Please wait before sending more messages.")
            return None
        
        response = self.get_response(request)
        return response
    

class RolepermissionMiddleware:
    """
    A middleware that checks the user’s role i.e admin, before allowing access to specific actions
    """
    def __init__(self, get_response):
            self.get_response = get_response
            self.allowed_roles = ["admin", "moderator"]

    def __call__(self, request):
        user = request.user
        # Check if the user is authenticated and has the required role
        if user.is_authenticated and (user.role not in self.allowed_roles):
            return f"Access denied: this action requires {self.allowed_roles} privilages"

        return self.get_response(request)