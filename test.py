import asyncio
import asyncpg

async def test():
    conn = await asyncpg.connect("postgresql://postgres:postgres@localhost:5432/miniwarehouse")
    print("OK")
    await conn.close()

asyncio.run(test())
