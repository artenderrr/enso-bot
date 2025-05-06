# mypy: disable-error-code="import-untyped"
from __future__ import annotations
from typing import Any, ClassVar, cast
import json
from uuid import uuid4
from pathlib import Path
from dataclasses import dataclass
import asyncpg
import aiofiles
from core import get_pg_pool

@dataclass
class ClothingItem:
    _images_dir: ClassVar[Path] = Path("images/items")

    id: int
    name: str
    collection: str
    volume: int
    image_path: Path

    @classmethod
    async def _save_item_image(cls, image_bytes: bytes, image_extension: str) -> Path:
        cls._images_dir.mkdir(parents=True, exist_ok=True)
        image_path = cls._images_dir / f"{uuid4()}{image_extension}"
        async with aiofiles.open(image_path, "wb") as file:
            await file.write(image_bytes)
        return image_path

    @classmethod
    async def _save_in_database(
        cls, name: str, collection: str, volume: int, image_path: Path
    ) -> int:
        async with get_pg_pool().acquire() as conn:
            item_id = await conn.fetchval(
                (
                    "INSERT INTO items (name, collection, volume, image_path) "
                    "VALUES ($1, $2, $3, $4) "
                    "RETURNING id"
                ),
                name, collection, volume, str(image_path)
            )
        return cast(int, item_id)

    @staticmethod
    def _parse_row_data(row: asyncpg.Record) -> dict[str, Any]:
        item_data = dict(row)
        item_data["image_path"] = Path(item_data["image_path"])
        return item_data

    @classmethod
    async def create(
        cls,
        name: str,
        collection: str,
        volume: int,
        image_bytes: bytes,
        image_extension: str
    ) -> ClothingItem:
        image_path = await cls._save_item_image(image_bytes, image_extension)
        item_id = await cls._save_in_database(name, collection, volume, image_path)
        return cls(item_id, name, collection, volume, image_path)

    @classmethod
    async def get(cls, item_id: int) -> ClothingItem | None:
        async with get_pg_pool().acquire() as conn:
            item_row = await conn.fetchrow(
                "SELECT * FROM items WHERE id = $1", item_id
            )
        if item_row:
            item_data = ClothingItem._parse_row_data(item_row)
            return cls(**item_data)
        return None

    @classmethod
    async def all(cls) -> list[ClothingItem]:
        async with get_pg_pool().acquire() as conn:
            item_rows = await conn.fetch("SELECT * FROM items")
        items_data = [ClothingItem._parse_row_data(row) for row in item_rows]
        return [cls(**item_data) for item_data in items_data]

    @property
    def json(self) -> str:
        item_data = self.__dict__
        item_data["image_path"] = str(item_data["image_path"])
        return json.dumps(item_data)

    async def delete(self) -> None:
        async with get_pg_pool().acquire() as conn:
            await conn.execute(
                "DELETE FROM items WHERE id = $1", self.id
            )
        self.image_path.unlink(missing_ok=True)
