from seed import connect_to_prodev
import sys

def stream_user_ages():
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users"
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def ages():
    user_ages = stream_user_ages()
    for age in user_ages:
        yield age

if __name__ == "__main__":
    total = 0
    count = 0
    for row in ages():
        age = int(row.get("age"))
        total += age
        count += 1
    print(f"Average age of users : {round(total / count)}")
        