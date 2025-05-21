import sqlite3
import functools
from datetime import datetime

#### decorator to lof SQL queries

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwags):
        print (func(*args, **kwags))

    return wrapper


@log_queries
def fetch_all_users(query):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
    except sqlite3.Error as e:
         print(e)
    conn.close()
    return results
#### fetch users while logging the query
fetch_all_users(query="SELECT * FROM users")
