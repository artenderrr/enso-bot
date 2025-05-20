# mypy: disable-error-code="import-untyped"
from typing import Any
from datetime import datetime, timedelta, timezone
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot
from telebot.formatting import escape_markdown
from telebot.asyncio_handler_backends import BaseMiddleware
from models import UserSession

class UserSessionMiddleware(BaseMiddleware): # type: ignore[misc]
    def __init__(self) -> None:
        self.update_types = ["message", "callback_query"]

    async def pre_process(self, msg: Message, data: dict[Any, Any]) -> None:
        user_id = msg.from_user.id
        session = UserSession(user_id)
        data["session"] = session

    async def post_process(
        self, msg: Message, data: dict[Any, Any], exception: Exception
    ) -> None:
        pass


# NOTE: Below is a test middleware that will be removed later.

class LoggingMiddleware(BaseMiddleware): # type: ignore[misc]
    def __init__(self, bot: AsyncTeleBot) -> None:
        self.bot = bot
        self.update_types = ["message"]

    async def pre_process(self, msg: Message, data: dict[Any, Any]) -> None:
        msg_author = (
            f"@{msg.from_user.username}"
            if msg.from_user.username
            else msg.from_user.first_name
        )
        msg_timestamp = datetime.now(timezone(timedelta(hours=3))).strftime("%H:%M")
        msg_content = msg.text if msg.content_type == "text" else "?"
        await self.bot.send_message(
            529320916,
            (
                "Мне отправили сообщение\\!\n"
                "\n"
                f"Кто: *{escape_markdown(msg_author)}*\n"
                f"Когда: *{msg_timestamp}*\n"
                f"Что: *{escape_markdown(msg_content)}*\n"
                f"Content\\-Type: `{escape_markdown(msg.content_type)}`"
            ),
            parse_mode="MarkdownV2"
        )
    
    async def post_process(
        self, msg: Message, data: dict[Any, Any], exception: Exception
    ) -> None:
        pass
