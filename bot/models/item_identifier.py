from typing import cast
from dataclasses import dataclass
from core import get_pg_pool

@dataclass
class ItemIdentifier:
    id: str
    item_id: int
    owner: str
    purchase_date: str
    owner_note: str | None

    @classmethod
    async def exists(cls, id_: str) -> bool:
        async with get_pg_pool().acquire() as conn:
            exists = await conn.fetchval(
                "SELECT EXISTS ("
                    "SELECT 1 "
                    "FROM identifiers "
                    "WHERE id = $1"
                ")", id_
            )
        return cast(bool, exists)
