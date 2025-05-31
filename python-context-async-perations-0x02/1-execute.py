import sqlite3

# context manager class for executing SQL queries on an SQLite database.
class ExecuteQuery:
    def __init__(self, db, query):
        self.db = db
        self.conn = None
        self.cursor = None
        self.result = None
        self.query = query

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db)
            self.cursor = self.conn.cursor()
            self.cursor.execute(self.query)
            self.result = self.cursor.fetchall()
            return self.result
        except sqlite3.Error as e:
            print(f"Error: {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
 
param = 20
query = f"SELECT * FROM users WHERE age < {param}"

with ExecuteQuery('users.db',query) as result:
    for row in result:
        print(row)
