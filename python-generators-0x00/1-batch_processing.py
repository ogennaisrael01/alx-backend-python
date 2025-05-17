from seed import connect_to_prodev


#a function stream_users_in_batches(batch_size) that fetches rows in batches
def stream_users_in_batches(batch_size):
    connection = connect_to_prodev() #connect to database
    cursor = connection.cursor()
    offset = 0
    while True:
        print("grouping in batch")
        cursor.execute(
            "SELECT * FROM user_data ORDER BY user_id LIMIT %s OFFSET %s", (batch_size, offset)
        )
        rows = cursor.fetchall()
        if not rows:
            break
        for row in rows:
            
            yield {
                'Name': row[1],
                'email': row[2],
                'Age': row[3]
            }
        offset += batch_size
    cursor.close()
    connection.close()

for user in stream_users_in_batches(100):
    print(user)


#a function batch_processing() that processes each batch to filter users over the age of25`
def batch_processing(batch_size):
    connection = connect_to_prodev()# connect to database
    cursor = connection.cursor()
    offset = 0
    batches = []
    while True:
        cursor.execute(
            "SELECT * FROM user_data WHERE user_data.age > 25  ORDER BY user_id LIMIT %s OFFSET %s ", (batch_size, offset)
        )
        rows = cursor.fetchall()
        if not rows:
            break
        batch = []
        for row in rows:
            batch.append({
                'Name': row[1],
                'email': row[2],
                'Age': row[3]
            })
        batches.append(batch)
        offset += batch_size
    cursor.close()
    connection.close()
    return batches[1]

print(batch_processing(100))