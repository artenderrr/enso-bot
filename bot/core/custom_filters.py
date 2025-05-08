# mypy: disable-error-code="import-untyped"
from telebot.types import Message, CallbackQuery
from telebot.asyncio_filters import SimpleCustomFilter
from telebot.asyncio_filters import AdvancedCustomFilter
from .config import bot_config
from models import UserSession

class AdminFilter(SimpleCustomFilter): # type: ignore[misc]
    key = "is_admin"

    @staticmethod
    async def check(msg: Message) -> bool:
        user_id = msg.from_user.id
        return user_id in bot_config.admin_user_ids

class StateFilter(AdvancedCustomFilter): # type: ignore[misc]
    key = "state"

    @staticmethod
    async def check(msg: Message, text: str) -> bool:
        user_id = msg.from_user.id
        session = UserSession(user_id)
        state = await session.get_state()
        return state == text

class CallbackQueryFilter(AdvancedCustomFilter): # type: ignore[misc]
    key = "callback"

    @staticmethod
    async def check(call: CallbackQuery, filter_value: str | list[str]) -> bool:
        if isinstance(filter_value, list):
            return any(value == call.data for value in filter_value)
        return call.data == filter_value
