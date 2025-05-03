# mypy: disable-error-code="import-untyped"
from telebot.async_telebot import AsyncTeleBot
from .custom_filters import AdminFilter
from .config import bot_config as config
from .storage import get_redis

__all__ = ["config", "get_redis"]

def register_custom_filters(bot: AsyncTeleBot) -> None:
    bot.add_custom_filter(AdminFilter())
