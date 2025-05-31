import time
import sqlite3 
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwags):
        try:
            conn = sqlite3.connect('users.db')
            print(func(conn, *args, **kwags))
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

    return wrapper
 # A function that fetches users from the database, retrying on failure.
def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(conn, *args, **kwags):
            attempts = 0
            while attempts < retries:
                try:
                    result = func(conn, *args, **kwags)
                    return result
                    
                except sqlite3.Error as e:
                    print(f"Error {e}- retrying.....")
                    time.sleep(delay)
                attempts += 1
            if sqlite3.Error:
                print("Can't load ..")
        return wrapper
    return decorator





@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user")
    return cursor.fetchall()

    #### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
