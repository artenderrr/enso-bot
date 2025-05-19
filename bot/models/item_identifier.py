from __future__ import annotations
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

    @classmethod
    async def create(
        cls,
        id_: str,
        item_id: int,
        owner: str,
        purchase_date: str,
        owner_note: str
    ) -> ItemIdentifier:
        async with get_pg_pool().acquire() as conn:
            await conn.execute(
                "INSERT INTO identifiers "
                "(id, item_id, owner, purchase_date, owner_note) "
                "VALUES "
                "($1, $2, $3, $4, $5)",
                id_, item_id, owner, purchase_date, owner_note
            )
        return cls(id_, item_id, owner, purchase_date, owner_note)
