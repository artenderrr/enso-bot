# mypy: disable-error-code="import-untyped"
from telebot.async_telebot import AsyncTeleBot
from .add_item import register_add_item_handlers
from .del_item import register_del_item_handlers
from .view_items import register_view_items_handlers
from .restricted import register_restricted_operation_handlers

def register_message_handlers(bot: AsyncTeleBot) -> None:
    register_add_item_handlers(bot)
    register_del_item_handlers(bot)
    register_view_items_handlers(bot)
    register_restricted_operation_handlers(bot)
