import sqlite3


class DatabaseConnection:
    def __init__(self, db_name: str): 
        self.db_connection = sqlite3.connect(db_name)
    
    def __enter__(self):
        print("Connection")
        return self.db_connection
    def __exit__(self, type, value, traceback):
        print("Exited")
        self.db_connection.close()
    
if __name__ == "__main__":
    with DatabaseConnection("users.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        print(result)
        