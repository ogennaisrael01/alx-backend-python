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


query_cache = {}
def cache_query(func):

    @functools.wraps(func)
    def wrapper(*args, **kwags):
        query = args[0]
        if query is None:# if no query
            print("Error: NO SQL query")
            return func(*args, **kwags)
        #check cache first
        if query in query_cache:
            print(f"Returning cache result for query {query}")
            return query_cache[query]
        
        else: 
            print(f"catch missed: {query}")
            result = func(*args, **kwags)
            query_cache[query] = result
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()



#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")