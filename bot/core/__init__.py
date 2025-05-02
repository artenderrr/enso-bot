# mypy: disable-error-code="import-untyped"
from telebot.async_telebot import AsyncTeleBot
from .custom_filters import AdminFilter
from .config import bot_config as config

__all__ = ["config"]

def register_custom_filters(bot: AsyncTeleBot) -> None:
    bot.add_custom_filter(AdminFilter())
