# mypy: disable-error-code="import-untyped"
from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool
import asyncpg
from asyncpg.pool import Pool
from .config import bot_config

redis_pool = ConnectionPool(host="redis", port=6379, decode_responses=True)
_pg_pool = None

PG_TABLES_INIT_SQL = """
CREATE TABLE IF NOT EXISTS items (
    id INT GENERATED ALWAYS AS IDENTITY,
	name VARCHAR(64) NOT NULL,
	collection VARCHAR(64) NOT NULL,
	volume INT NOT NULL CHECK(volume > 0),
	image_path VARCHAR(64) NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS identifiers (
    id VARCHAR(5) CHECK(id ~ '^\\d{5}$'),
    item_id INT NOT NULL,
    owner VARCHAR(64) NOT NULL,
    purchase_date VARCHAR(10) CHECK(purchase_date ~ '^\\d{2}\\.\\d{2}\\.\\d{4}$') NOT NULL,
    owner_note VARCHAR(64),
    added_at TIMESTAMP DEFAULT now() NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (item_id) REFERENCES items (id)
        ON DELETE CASCADE
);
"""

def get_redis() -> Redis:
    return Redis(connection_pool=redis_pool) # type: ignore[no-any-return]

def get_pg_pool() -> Pool:
    if not _pg_pool:
        raise RuntimeError("Database pool is not initialized")
    return _pg_pool

async def create_pg_pool() -> None:
    global _pg_pool
    _pg_pool = await asyncpg.create_pool(bot_config.db_url)

async def create_pg_tables() -> None:
    async with get_pg_pool().acquire() as conn:
        await conn.execute(PG_TABLES_INIT_SQL)

async def init_pg() -> None:
    await create_pg_pool()
    await create_pg_tables()
