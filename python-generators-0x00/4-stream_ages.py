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
    save_ages_in_list = list()
    for row in ages():
        save = int(row.get("age"))
        save_ages_in_list.append(save)
    avg = sum(save_ages_in_list) / len(save_ages_in_list)
    print(f"Average age of users: {round(avg, 2)}")
