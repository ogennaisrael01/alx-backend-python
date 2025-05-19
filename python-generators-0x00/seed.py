import pymysql
from pymysql import Error
import csv

# connect to database server
def connect_db():
    try:
        conn = pymysql.connect(
            host= 'localhost',
            user='root',
            password='193782',
        )
        print("connected to my MYSQL server")
        return conn
    except pymysql.Error as error:
        print(f"Error connecting the server: {error}")
        return None
        
    conn.close()

# Create database
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
                    CREATE DATABASE ALX_prodev;""")

        print("successfuly created a database")

    except pymysql.Error as error:
        print("database exits")
    cursor.close()

# connect to database
def connect_to_prodev():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='193782',
            database='ALX_prodev'
        )
        print("database connected successully")
        return conn
    except pymysql.Error as error:
        print(f"error in connecting to database {error}")
        return None
    conn.close()
# creaate table
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
                       CREATE TABLE user_data(
                       user_id INT AUTO_INCREMENT PRIMARY KEY,
                       name VARCHAR(100),
                       email VARCHAR(100),
                       age INT
                       );""")
        
        print("Table created successfully")

    except pymysql.Error as error:
        print(f"Error creating table: {error}")
        return None
    cursor.close()

# insert data into the database
def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                sql = "INSERT INTO user_data(name, email, age) VALUES (%s, %s, %s)"
                cursor.execute(sql, (row[0], row[1], row[2]))
        connection.commit()
        print("data inserted successully")
    except pymysql.Error as error:
        print ("error inserting data")

    cursor.close()



    


def main():
    # Connect to MySQL server (no database yet)
    server_conn = connect_db()
    if server_conn:
        create_database(server_conn)
        server_conn.close()

    # Connect to the new database
    db_conn = connect_to_prodev()
    if db_conn:
        create_table(db_conn)
        # Insert sample data
        # sample_data = ("user_data.csv")
        # insert_data(db_conn, "user_data.csv")
       


if __name__ == "__main__":
    main()

    
   