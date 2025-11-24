import requests
from requests.auth import HTTPBasicAuth
from chats.utils.retry_on_failures import Log


def run_request():
    # email = "ogennaisrael@gmail.com"
    # password = "0987poiu"
    # url = "http://localhost:8000/api/v1/conversation/"
    # payload  = {
    #     "name": "Hackathon Preparations",
    #     "description": "Preparations for the upcoming hackathons"
    # }

    # response = requests.post(url, data=payload, auth=HTTPBasicAuth(username=email, password=password))
    # if response.status_code == 201:
    #     print("success")
    #     print(response.json())
    # else:
    #     print("Unsuccessfull")
    #     print(response.status_code, response.text)

    message = "Hello world"

    with Log("example.log", "a") as log_error:
        log_error.write(f"{message} \n")
if __name__ == "__main__":
    run_request()