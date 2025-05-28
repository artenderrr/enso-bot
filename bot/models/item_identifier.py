# mypy: disable-error-code="import-untyped"
from __future__ import annotations
from typing import Any
from typing import cast
from dataclasses import dataclass
import asyncpg
from core import get_pg_pool

@dataclass
class ItemIdentifier:
    id: str
    item_id: int
    owner: str
    purchase_date: str
    owner_note: str | None

    @staticmethod
    def _parse_row_data(row: asyncpg.Record) -> dict[str, Any]:
        return {k: v for k, v in row.items() if k != "added_at"}

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

    @classmethod
    async def get(cls, id_: str) -> ItemIdentifier | None:
        async with get_pg_pool().acquire() as conn:
            identifier_row = await conn.fetchrow(
                "SELECT * FROM identifiers WHERE id = $1", id_
            )
        if identifier_row:
            identifier_data = ItemIdentifier._parse_row_data(identifier_row)
            return cls(**identifier_data)
        return None

    @classmethod
    async def get_many(
        cls,
        *,
        offset: int = 0,
        limit: int | None = None
    ) -> list[ItemIdentifier]:
        async with get_pg_pool().acquire() as conn:
            rows = await conn.fetch(
                "SELECT * "
                "FROM identifiers "
                "ORDER BY added_at DESC "
                "OFFSET $1 "
                f"{'LIMIT $2' if limit is not None else ''}",
                *filter(lambda x: x is not None, (offset, limit))
            )
        identifiers = [cls(**ItemIdentifier._parse_row_data(row)) for row in rows]
        return identifiers

    async def delete(self) -> None:
        async with get_pg_pool().acquire() as conn:
            await conn.execute(
                "DELETE FROM identifiers WHERE id = $1", self.id
            )
