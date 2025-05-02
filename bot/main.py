# mypy: disable-error-code="import-untyped"
import asyncio
from telebot.async_telebot import AsyncTeleBot
from handlers import register_handlers
from core import config, register_custom_filters

bot = AsyncTeleBot(config.bot_token)

register_handlers(bot)
register_custom_filters(bot)

asyncio.run(bot.polling())
