# mypy: disable-error-code="import-untyped"
from telebot.async_telebot import AsyncTeleBot
from .seed import seed_db
from .config import bot_config as config
from .storage import get_redis, init_pg, get_pg_pool

__all__ = ["seed_db", "config", "get_redis", "init_pg", "get_pg_pool"]

def register_custom_filters(bot: AsyncTeleBot) -> None:
    from telebot.asyncio_filters import TextMatchFilter
    from .custom_filters import (
        AdminFilter,
        StateFilter,
        CallbackQueryFilter
    )
    custom_filters = (
        AdminFilter,
        StateFilter,
        TextMatchFilter,
        CallbackQueryFilter
    )
    for custom_filter in custom_filters:
        bot.add_custom_filter(custom_filter())

def register_middlewares(bot: AsyncTeleBot) -> None:
    from .middleware import (
        UserSessionMiddleware,
        LoggingMiddleware
    )
    bot.setup_middleware(UserSessionMiddleware())
    bot.setup_middleware(LoggingMiddleware(bot))
