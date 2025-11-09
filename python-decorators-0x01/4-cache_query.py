import time
import sqlite3 
import functools
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


query_cache = {}

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

def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        query = kwargs.get("query") if kwargs else None
        if query in query_cache.keys():
            logging.info(f"Duration {time.time() - start:.4f}s")
            return query_cache.get(query)
        else:
            response = func(*args, **kwargs)
            query_cache[query] = response
            logging.info(f"Duration {time.time() - start:.4f}s")
            return response
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == "__main__":
    #### First call will cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)
    #### Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print((users))