from seed import connect_to_prodev
from pymysql import Error

def stream_users():
    connection = connect_to_prodev()
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM user_data LIMIT 6;""")
    for row in cursor:
        yield({
            'Name': row[1],
            'email': row[2],
            'Age': row[3]
        })
    cursor.close()
    connection.close()
count_row = stream_users()
for row in count_row:
    print(row)