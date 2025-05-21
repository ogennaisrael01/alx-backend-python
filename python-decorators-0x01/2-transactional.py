"""This module demonstrates the use of Python decorators to manage database connections
and transactions automatically. It provides:
- A decorator to handle opening and closing SQLite database connections.
- A decorator to ensure that database operations are committed or rolled back as needed.
- An example function to update a user's email address in the database with automatic transaction handling.
"""


import sqlite3 
import functools

def with_db_connection(func):
    """
    Decorator to provide a SQLite database connection to the wrapped function.
    Ensures the connection is properly closed after use.
    """

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



def transactional(func):
    """
    Decorator to wrap a function in a database transaction.
    Commits the transaction if successful, rolls back on error.
    """
    def wrapper(conn, *args, **kwags):
        
        try:
           result = func(conn, *args, **kwags )
           conn.commit()
           return  result
        except sqlite3.Error as e:
            print("Error occured, rolling back....")
            print(e)
            conn.rollback()
    return wrapper


@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email):
    """
    Updates the email address of a user in the database.
    Args:
        conn: SQLite database connection.
        user_id: ID of the user to update.
        new_email: New email address to set.
    """ 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
    #### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Craford_Cartwright@hotmail.com')