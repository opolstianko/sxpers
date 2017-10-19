import aioredis

REDIS_HOST = 'localhost'


async def lookup_segment(mcmid):
    conn = await aioredis.create_connection(
        (REDIS_HOST, 6379))

    val = await conn.execute('get', mcmid)
    conn.close()
    await conn.wait_closed()

    if not val:
        return False

    return val


async def set_segment(mcmid, segment):
    conn = await aioredis.create_connection(
        (REDIS_HOST, 6379))

    await conn.execute('set', mcmid, segment)
    conn.close()
    await conn.wait_closed()

    return True
