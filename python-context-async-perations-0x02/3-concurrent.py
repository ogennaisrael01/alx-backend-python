
import aiosqlite
import asyncio

async def connect_db():
    try:
        db_connection = await aiosqlite.connect("users.db") 
        print("Connected to the users db successfully")
        return db_connection     
    except aiosqlite.Error as e:
        raise ValueError(e)

async def create_table():
    db = await connect_db()
    cursor = await db.cursor()
    await cursor.execute("SELECT * FROM users")
    result = await cursor.fetchall()
    print("Executed sql query for fetching user data")
    await cursor.close()
    await db.close()
    return result




async def main():
    task = await asyncio.gather(connect_db(), create_table())
    print(task)

if __name__ == "__main__":   
    asyncio.run(main())