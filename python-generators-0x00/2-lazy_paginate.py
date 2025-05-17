from seed import connect_to_prodev
def paginate_users(page_size, offset=0):
    
    connection = connect_to_prodev()#connect to database
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    result = cursor.fetchall()
    yield result


for page in (paginate_users(100)):
   print(page)
