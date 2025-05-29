# mypy: disable-error-code="import-untyped"
import asyncio
from telebot.async_telebot import AsyncTeleBot
from handlers import register_handlers
from core import (
    config,
    seed_db,
    init_pg,
    register_custom_filters,
    register_middlewares
)

bot = AsyncTeleBot(config.bot_token)

register_handlers(bot)
register_custom_filters(bot)
register_middlewares(bot)

async def main() -> None:
    await init_pg()
    await seed_db()
    await bot.polling()

asyncio.run(main())
