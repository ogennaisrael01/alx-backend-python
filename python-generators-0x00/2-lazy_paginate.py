from seed import connect_to_prodev
def lazy_paginate(page_size, offset):
    
    connection = connect_to_prodev()#connect to database
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    result = cursor.fetchall()
    yield result


for page in (lazy_paginate(100, 0)):
   print(page)
