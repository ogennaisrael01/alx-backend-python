
import aiosqlite
import asyncio

async def connect_db():
    try:
        db_connection = await aiosqlite.connect("users.db") 
        print("Connected to the users db successfully")
        return db_connection     
    except aiosqlite.Error as e:
        raise ValueError(e)

async def async_fetch_users():
    db = await connect_db()
    cursor = await db.cursor()
    await cursor.execute("SELECT * FROM users")
    result = await cursor.fetchall()
    print("Executed sql query for fetching user data")
    await cursor.close()
    await db.close()
    return result

async def async_fetch_older_users():
    db = await  connect_db()
    cursor =await db.cursor()
    await cursor.execute("SELECT * FROM users WHERE age > 40")
    result = await cursor.fetchall()
    print("Fetched user data who's age are greater than 40")
    await cursor.close()
    await db.close()
    return result




async def main():
    result = await asyncio.gather(async_fetch_older_users(), async_fetch_users())
    for task in result:
        print(task)

if __name__ == "__main__":   
    asyncio.run(main())