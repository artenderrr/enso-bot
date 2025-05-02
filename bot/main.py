# mypy: disable-error-code="import-untyped"
import asyncio
from telebot.async_telebot import AsyncTeleBot
from core.config import Config

bot = AsyncTeleBot(Config.bot_token)

asyncio.run(bot.polling())
