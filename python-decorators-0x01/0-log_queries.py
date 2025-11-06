import sqlite3
from sqlite3 import Connection
import functools   
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        query = kwargs.get("query")
        logging.info(f"funtion name: {func.__name__}")
        logging.info(f"Executing query: {query} ")
        response = func(*args, **kwargs)

        end = datetime.now()
        duration = end - start
        logging.info(f"Execution time: {duration.total_seconds():.4f}s")
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
def seed_db(query):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    return "Seeded db successfull"

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    # table = create_table(query="CREATE TABLE users ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT UNIQUE, age INT) STRICT")
    # print(table)
    # query = "INSERT INTO users (name, email, age) VALUES ('ogenna', 'ogennaisrael@gmail.com', 21)"
    # seed = seed_db(query=query)
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)