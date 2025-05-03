# mypy: disable-error-code="import-untyped"
from typing import Any
from telebot.types import Message
from telebot.asyncio_handler_backends import BaseMiddleware
from models import UserSession

class UserSessionMiddleware(BaseMiddleware): # type: ignore[misc]
    def __init__(self) -> None:
        self.update_types = ["message"]

    async def pre_process(self, msg: Message, data: dict[Any, Any]) -> None:
        user_id = msg.from_user.id
        session = UserSession(user_id)
        data["session"] = session

    async def post_process(
        self, msg: Message, data: dict[Any, Any], exception: Exception
    ) -> None:
        pass
