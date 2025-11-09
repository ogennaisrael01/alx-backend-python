import sqlite3

class ExecuteQuery:
    def __init__(self, query, parameter):
        self.db_connection = sqlite3.connect("users.db")
        self.query = query
        self.params = parameter

    def __enter__(self):
        cursor = self.db_connection.cursor()
        cursor.execute(self.query, (self.params,))
        result = cursor.fetchall()
        return result
    
    def __exit__(self, type, value, traceback):
        self.db_connection.close()


if __name__ == "__main__":
    params = 25
    query = "SELECT  * FROM users WHERE ae > ?"
    with ExecuteQuery(query, parameter=params) as execute:
        print(execute)
    