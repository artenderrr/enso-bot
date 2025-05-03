from typing import Any, cast
import json
from core import get_redis

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
