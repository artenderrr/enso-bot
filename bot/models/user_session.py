# mypy: disable-error-code="import-untyped"
from __future__ import annotations
from typing import Any, Awaitable, Callable, cast
import json
from math import ceil
from telebot.types import InputMediaPhoto
from core import get_redis, config
from models.item_identifier import ItemIdentifier
from handlers.replies import get_view_items_msg_success
from .clothing_item import ClothingItem

class StateError(Exception):
    def __init__(self, *, current: str, required: str) -> None:
        super().__init__(
            f"Current state is '{current}', should be '{required}'"
        )

class UserSession:
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        self.redis = get_redis()

    async def get_state(self) -> str:
        state = await self.redis.get(
            f"user:{self.user_id}:state"
        )
        return state or "default"

    async def set_state(self, new_state: str) -> None:
        await self.redis.set(
            f"user:{self.user_id}:state",
            new_state,
            ex=600
        )

    async def clear_state(self) -> None:
        await self.redis.delete(
            f"user:{self.user_id}:state"
        )

    async def get_context(self) -> dict[str, Any]:
        raw_context = await self.redis.get(
            f"user:{self.user_id}:context"
        ) or "{}"
        context = cast(dict[str, Any], json.loads(raw_context))
        return context

    async def update_context(self, update_data: dict[str, Any]) -> None:
        context = await self.get_context()
        context.update(update_data)
        raw_context = json.dumps(context)
        await self.redis.set(
            f"user:{self.user_id}:context",
            raw_context,
            ex=600
        )

    async def clear_context(self) -> None:
        await self.redis.delete(
            f"user:{self.user_id}:context"
        )

    async def set_view_items_context(self, items: list[ClothingItem]) -> None:
        await self.update_context({
            "current_item": 1,
            **{f"item_{i}": item.json for i, item in enumerate(items, start=1)},
            "items_count": len(items)
        })

    async def get_current_view_item(self) -> ClothingItem | None:
        state = await self.get_state()
        if state != "view_items":
            return None
        context = await self.get_context()
        item_data = json.loads(context[f"item_{context['current_item']}"])
        return ClothingItem(**item_data)

    async def get_current_view_item_media(self) -> InputMediaPhoto:
        current_item = await self.get_current_view_item()
        current_item_image = await current_item.load_image_bytes()
        return InputMediaPhoto(
            current_item_image,
            get_view_items_msg_success(current_item.__dict__),
            parse_mode="MarkdownV2"
        )

    @staticmethod
    def require_state(required_state: str) -> Callable:                 # type: ignore[type-arg]
        def decorator(func: Callable[..., Awaitable[Any]]) -> Callable: # type: ignore[type-arg]
            async def wrapper(self: UserSession, *args: Any, **kwargs: Any) -> Any:
                state = await self.get_state()
                if state != required_state:
                    raise StateError(current=state, required=required_state)
                result = await func(self, *args, **kwargs)
                return result
            return wrapper
        return decorator

    @require_state("view_items")
    async def decrement_current_view_item(self) -> None:
        context = await self.get_context()
        decremented_current_item = context["current_item"] - 1
        if decremented_current_item < 1:
            decremented_current_item = context["items_count"]
        await self.update_context({
            "current_item": decremented_current_item
        })

    @require_state("view_items")
    async def increment_current_view_item(self) -> None:
        context = await self.get_context()
        incremented_current_item = context["current_item"] + 1
        if incremented_current_item > context["items_count"]:
            incremented_current_item = 1
        await self.update_context({
            "current_item": incremented_current_item
        })

    @require_state("view_ids")
    async def get_current_view_ids_page(self) -> list[ItemIdentifier]:        
        context = await self.get_context()
        current_page = context["current_view_ids_page"]
        current_page_identifiers = await ItemIdentifier.get_many(
            offset=(current_page - 1) * config.view_ids_page_size,
            limit=config.view_ids_page_size
        )
        return current_page_identifiers

    @require_state("view_ids")
    async def decrement_current_view_ids_page(self) -> None:
        context = await self.get_context()
        page_count = ceil(await ItemIdentifier.count() / config.view_ids_page_size)
        current_page = context["current_view_ids_page"]        
        decremented_current_page = current_page - 1
        if (
            decremented_current_page < 1 or
            decremented_current_page > page_count
        ):
            decremented_current_page = page_count
        await self.update_context({
            "current_view_ids_page": decremented_current_page
        })

    @require_state("view_ids")
    async def increment_current_view_ids_page(self) -> None:
        context = await self.get_context()
        page_count = ceil(await ItemIdentifier.count() / config.view_ids_page_size)
        current_page = context["current_view_ids_page"]        
        incremented_current_page = current_page + 1
        if incremented_current_page > page_count:
            incremented_current_page = 1
        await self.update_context({
            "current_view_ids_page": incremented_current_page
        })

    async def clear_session(self) -> None:
        await self.clear_state()
        await self.clear_context()
