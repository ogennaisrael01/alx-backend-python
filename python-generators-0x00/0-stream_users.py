from seed import connect_to_prodev
import sys

def stream_users():
    connection = connect_to_prodev()
    if not connection:
        raise ValueError("Unable to connect to db")
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM users ORDER BY name"
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            yield(row)
    except Exception:
        raise ValueError("error occured while streaming user data")
    finally:
        connection.close()
        cursor.close()

if __name__ == "__main__":
    print(next(stream_users()))
