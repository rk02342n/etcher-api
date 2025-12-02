# import asyncio
# import asyncpg

# async def test_connection():
#     try:
#         conn = await asyncpg.connect(
#             'postgresql://myuser:mypassword@localhost:5432/blogchain_db'
#         )
#         print("Connection successful!")
#         await conn.close()
#     except Exception as e:
#         print(f"Connection failed: {e}")

# asyncio.run(test_connection())

import asyncio
import asyncpg

async def run():
    conn = await asyncpg.connect('postgresql://myuser:mypassword@localhost:5432/etcher_db')
    values = await conn.fetch(
        'SELECT * FROM authors'
    )
    await conn.close()

asyncio.run(run())