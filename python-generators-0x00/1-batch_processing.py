from seed import connect_to_prodev

def get_connection():
    connection = connect_to_prodev()
    if connection:
        return connection
    return False

def stream_users_in_batches(batch_size):
    connection = get_connection()
    if not connection:
        return "Please connect to you database"
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM user_data"
        cursor.execute(query)
        result = cursor.fetchmany(size=batch_size)
        for row in result:
            yield row
    except Exception as e:
        raise ValueError(f"Error: {e}")
    finally:
        connection.close()
        cursor.close()


def batch_processing(batch_size):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM users WHERE age > 25"
        cursor.execute(query)
        result = cursor.fetchmany(size=batch_size)
        for row in result:
            yield row
    except Exception as e:
        raise ValueError(f"error: {e}")
    finally:
        connection.close()
        cursor.close()
    
if __name__ == "__main__":
    if get_connection():
        for row in batch_processing(10):
            print(row)