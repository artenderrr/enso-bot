# mypy: disable-error-code="import-untyped"
from telebot.async_telebot import AsyncTeleBot
from .add_item import register_add_item_handlers
from .del_item import register_del_item_handlers

def register_message_handlers(bot: AsyncTeleBot) -> None:
    register_add_item_handlers(bot)
    register_del_item_handlers(bot)
