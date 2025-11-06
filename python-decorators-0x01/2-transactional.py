import sqlite3 
from sqlite3 import Connection
import functools
import logging 

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

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

def transactional(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):  
        conn = args[0] if args else None
        if not conn:
            raise ValueError("Connection object was not found")
        try:
            response = func(*args, **kwargs)
            conn.commit()
            return response
        except sqlite3.Error as e:
            print("Error occured")
            conn.rollback()
            logging.error(f"error occured while updatting db : {e}")
            raise
        
    return wrapper



@with_db_connection 
@transactional 
def update_user_email(conn: Connection, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


    #### Update user's email with automatic transaction handling 
if __name__ == "__main__":
    user_id = 1
    print(update_user_email(user_id = user_id, new_email=39393939))