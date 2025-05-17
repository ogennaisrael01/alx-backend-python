import pymysql
from pymysql import Error

def stream_users():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='193782',
        database='ALX_prodev'
    )
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT * FROM user_data LIMIT 6;""")
        for row in cursor:
            yield({
                'Name': row[1],
                'email': row[2],
                'Age': row[3]
            })
    except pymysql.Error as error:
        print(f"can't load file {error}")

count_row = stream_users()
for row in (count_row):
    print(row)