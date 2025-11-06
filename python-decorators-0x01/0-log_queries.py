import sqlite3
from sqlite3 import Connection
import functools   
import time 
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        query = kwargs.get("query")
        print("funtion name:", func.__name__)
        logging.info(f"Executing query: {query} ")
        response = func(query)


        duration = time.time() - start
        print(f"Execution time: {duration:2f}s")
        return response
        
    return wrapper

@log_queries
def create_table(query):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    return "Tables created successfully"


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    # table = create_table(query="CREATE TABLE users (name VARCHAR(100), email VARCHAR(100), age INT)")
    # print(table)
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)