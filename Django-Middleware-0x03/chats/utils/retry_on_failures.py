import logging
import csv
import time


class LogLoggings:
    def __init__(self, file_name, method):
        self.file_name = open(file_name, mode=method, newline="")

    def __enter__(self):
        return self.file_name

    def __exit__(self, type, value, traceback):
        self.file_name.close()
        
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retry_on_failures(google_payload):
    attempts = 0
    number_of_retries = 5

    for _ in range(number_of_retries):
        try:
            if google_payload:
                return google_payload
        except (Exception, ValueError) as e:
            msg = logging.error(f"Error occured: {e}")   
        if attempts < number_of_retries:
            time.sleep(5)
        attempts += 1
        with LogLoggings("loggings.csv", "w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(msg)
        