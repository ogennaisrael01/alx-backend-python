from seed import connect_to_prodev

def stream_user_ages():
    connection = connect_to_prodev() #connect to database
    cursor = connection.cursor()
    cursor.execute("""SELECT age FROM user_data;""")
    result = cursor.fetchall()
    for age_row in result:
        yield(
            {'Age': age_row}
            )
for row in stream_user_ages():
    print(row)


def calculate_average():
    connection = connect_to_prodev() #connect to database
    cursor = connection.cursor()
    cursor.execute("""SELECT AVG(age) FROM user_data;""")
    result = cursor.fetchall()
    for age_row in result:
        print(
            {'Average_age': age_row}
            )
        
calculate_average()