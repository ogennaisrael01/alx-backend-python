import sqlite3
#context manager class for handling SQLite database connections.
class DatabaseConnection:
    def __init__(self, database):
        self.database = database
        self.conn = None

    def __enter__(self):
        # connect to sqlite database
        try:
            self.conn = sqlite3.connect(self.database)
            return self.conn
        except sqlite3.Error as e:
            print(f"Error: {e}")
    
    def  __exit__(self, exc_type, exc_val, exc_tb):
        #close databse
        if self.conn:
            self.conn.close()

with DatabaseConnection('users.db') as db:
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users") # fetch all table rows
        result = cursor.fetchall()
        for rows in  result:
            print(rows) # print rows from users table safely
        
    except sqlite3.Error as e:
        print(e) # handling errors
    