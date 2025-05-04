# mypy: disable-error-code="import-untyped"
from telebot.async_telebot import AsyncTeleBot
from .config import bot_config as config
from .storage import get_redis

__all__ = ["config", "get_redis"]

def register_custom_filters(bot: AsyncTeleBot) -> None:
    from telebot.asyncio_filters import TextMatchFilter
    from .custom_filters import AdminFilter, StateFilter
    custom_filters = (AdminFilter, StateFilter, TextMatchFilter)
    for custom_filter in custom_filters:
        bot.add_custom_filter(custom_filter())

def register_middlewares(bot: AsyncTeleBot) -> None:
    from .middleware import UserSessionMiddleware
    middlewares = (UserSessionMiddleware,)
    for middleware in middlewares:
        bot.setup_middleware(middleware())
