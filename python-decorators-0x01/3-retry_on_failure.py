import time
import sqlite3 
import functools
from sqlite3 import Connection
import logging
from  datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try :
            connection = sqlite3.connect("users.db")
            if connection:
                response = func(connection, *args, **kwargs)
        except sqlite3.Error as e:
            raise ValueError(f"Error: {e}")
        finally:
            connection.close()
        return response
    return wrapper


def retry_on_failure(retries, delay):
    def hold_func(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            start = datetime.now()
            logging.info(f"Operation started at: {start}")
            for _ in range(delay, retries + 1):
                try:
                    response = func(*args, **kwargs)
                    if response:
                        return response
                except sqlite3.Error as e:
                    logging.error(f"{e}")

                if attempts < retries:
                    time.sleep(5) 
                attempts += 1
            return f"Error occured, Check logs"
        return wrapper  
    return hold_func




@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn: Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

if __name__ == "__main__":
    users = fetch_users_with_retry()
    print(users)