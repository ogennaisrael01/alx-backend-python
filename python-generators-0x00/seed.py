from pathlib import Path
from dotenv import load_dotenv
import os
import psycopg2
import mysql.connector
import logging
from csv_reader import read_csv
import sys




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

database_user = os.getenv("database_user")
database_password = os.getenv("database_password")
database_name = os.getenv("database_name")


def connect_db():
    try:
        connection = mysql.connector.connect(
            user=database_user,
            password=database_password
        )
        logging.info("Successfully connected to MYSQL server")
        return connection
    except Exception as e:
        raise f"error: {e}"
    finally:
        ...
        

def create_database(connection):
    cursor = connection.cursor()
    try:
        query = "CREATE DATABASE IF NOT EXISTS ALX_prodev"
        cursor.execute(query)
        logging.info("Database ALX_prodev created successfully")
    except Exception as e:
        raise f"Error ocures {e}"
    finally:
        connection.close()
        cursor.close()
    

def test_db(connection):
    cursor = connection.cursor()
    try:
        query = "USE ALX_prodev"
        cursor.execute(query)
        if cursor:
            return True
        else:
            return False
    except Exception as e:
        raise ValueError(f"error {e}")
    finally:
        connection.close()
        cursor.close()

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            user=database_user,
            database=database_name,
            password=database_password
        )
        
        logging.info("Successfully connected the ALX_prodev database")
        return connection
    except Exception as e:
        raise ValueError(f"Error occured: {e}")


def create_table(connection):
    if not connection:
        logging.error("No database connection provided")
    
    cursor = connection.cursor()
    try:
        query = """CREATE TABLE users (
                            user_id VARCHAR(50) DEFAULT (UUID()) NOT NULL,
                            name VARCHAR(255) NOT NULL,
                            email VARCHAR(255) UNIQUE NOT NULL,
                            age DECIMAL NOT NULL,
                            PRIMARY KEY (user_id)
            
                        )"""
        cursor.execute(query)
        connection.commit()
        logging.info("Tables created successfully")
    except Exception as e:
        raise ValueError(f" Error: {e}")
    finally:
        connection.close()
        cursor.close()

def insert_data(connection, data):
    if not connection:
        raise ValueError
    if not data:
        raise ValueError
    
    cursor =  connection.cursor()

    if not cursor:
        return "cursor not connected"
    
    query = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
    for row in data:
        name = row[0]
        email = row[1]
        try: 
            age_str = row[2].strip()
            age = int(age_str)
        except Exception:
            logging.info("error converting age")
            age = None
        try:
            cursor.execute(query, (name, email, age))
            connection.commit()
        except Exception as e:
            return f"Error inserting : {e}"
    
    connection.close()
    cursor.close()


if __name__ == "__main__":
    ...
    # if connect_to_prodev():
    #     insert_data(connection=connect_to_prodev(), data=read_csv())