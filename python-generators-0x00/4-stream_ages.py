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
        
    cursor.close()

for row in stream_user_ages():
    print(row)




def calculate_average():
    connection = connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data;")
    ages = cursor.fetchall()
    total = 0
    count = 0
    for age_row in ages:
        total += age_row[0]
        count += 1
    average = total / count if count > 0 else 0
    print({'Average_age': average})
    cursor.close()    
calculate_average()