from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool

redis_pool = ConnectionPool(host="redis", port=6379, decode_responses=True)

def get_redis() -> Redis:
    return Redis(connection_pool=redis_pool) # type: ignore[no-any-return]
