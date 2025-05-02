# mypy: disable-error-code="import-untyped"
import asyncio
from telebot.async_telebot import AsyncTeleBot
from handlers import register_handlers
from core.config import Config

bot = AsyncTeleBot(Config.bot_token)
register_handlers(bot)

asyncio.run(bot.polling())
