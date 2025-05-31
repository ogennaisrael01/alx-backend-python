import aiosqlite
import  asyncio
import sqlite3
"""demonstrates asynchronous database operations using aiosqlite and asyncio.
"""

async def async_fetch_users():
    try:
        db = await aiosqlite.connect('users.db')
        cursor = db.cursor()
        cursor = cursor.execute('SELECT * FROM users')
        result = await cursor.fetchall() 
        for rows in result:
            print(rows)
    except ValueError as e:
        print(e)


async def async_fetch_older_users():
    db =  await aiosqlite.connect('users.db')
    cursor = db.cursor()
    cursor = cursor.execute('SELECT * FROM users WHERE age > 40 ')
    result  =  await cursor.fetchall()
    print( result)
    
    
async def fetch_concurrently():
    task =  await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return task

asyncio.run(fetch_concurrently())