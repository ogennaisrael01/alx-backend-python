import seed

def paginate_users(page_size, offset=0):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM users ORDER BY name LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_paginate(page_size):
    for row in paginate_users(page_size=page_size):
        yield row

if __name__ == "__main__":
    for row in lazy_paginate(10):
       print(row)