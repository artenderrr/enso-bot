# mypy: disable-error-code="import-untyped"
from __future__ import annotations
from typing import ClassVar, cast
from uuid import uuid4
from pathlib import Path
from dataclasses import dataclass
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

    @classmethod
    async def create(
        cls,
        name: str,
        collection: str,
        volume: int,
        image_bytes: bytes,
        image_extension: str
    ) -> ClothingItem:
        image_path = None
        try:
            image_path = await cls._save_item_image(image_bytes, image_extension)
            item_id = await cls._save_in_database(name, collection, volume, image_path)
        except Exception:
            if image_path and image_path.exists():
                image_path.unlink(missing_ok=True)
            raise
        return cls(item_id, name, collection, volume, image_path)

    @classmethod
    async def get(cls, item_id: int) -> ClothingItem | None:
        async with get_pg_pool().acquire() as conn:
            item_data = await conn.fetchrow(
                "SELECT * FROM items WHERE id = $1", item_id
            )
        return cls(**item_data) if item_data else None
