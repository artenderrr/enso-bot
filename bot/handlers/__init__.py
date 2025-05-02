# mypy: disable-error-code="import-untyped"
from telebot.async_telebot import AsyncTeleBot
from .commands import register_command_handlers

def register_handlers(bot: AsyncTeleBot) -> None:
    register_command_handlers(bot)
