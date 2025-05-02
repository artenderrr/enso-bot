# mypy: disable-error-code="import-untyped"
from telebot.types import Message
from telebot.asyncio_filters import SimpleCustomFilter
from .config import bot_config

class AdminFilter(SimpleCustomFilter): # type: ignore[misc]
    key = "is_admin"

    @staticmethod
    async def check(msg: Message) -> bool:
        user_id = msg.from_user.id
        return user_id in bot_config.admin_user_ids
