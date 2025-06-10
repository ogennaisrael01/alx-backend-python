from datetime import datetime
class RequestLoginMiddleware:
    """
    Create a middleware that logs each user’s requests to a file, including the timestamp, user and the request path.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response =  f"{datetime.now()} - {request.user} - {request.path}"

        with open("request.log", "a") as log_file:
            log_file.write(response)
        return self.get_response(request)