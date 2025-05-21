import sqlite3
import functools

#### decorator to lof SQL queries

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwags):
            func(*args, **kwags)

    return wrapper



def fetch_all_users(query):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
    except sqlite3.Error as e:
         print(e)
    print(results)

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")