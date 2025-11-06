from sqlite3 import Connection
import sqlite3
import functools
import datetime


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

@with_db_connection 
def get_user_by_id(conn: Connection, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchall() 

if __name__ == "__main__":
    user = get_user_by_id(user_id=1)
    print(user)