from datetime import datetime

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