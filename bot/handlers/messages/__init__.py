# mypy: disable-error-code="import-untyped"
from telebot.async_telebot import AsyncTeleBot
from .add_item import register_add_item_handlers
from .del_item import register_del_item_handlers
from .view_items import register_view_items_handlers
from .add_id import register_add_id_handlers
from .del_id import register_del_id_handlers
from .view_ids import register_view_ids_handlers
from .restricted import register_restricted_operation_handlers
from .unavailable import register_unavailable_operation_handlers
from .find_id import register_find_id_handlers

def register_message_handlers(bot: AsyncTeleBot) -> None:
    register_add_item_handlers(bot)
    register_del_item_handlers(bot)
    register_view_items_handlers(bot)
    register_add_id_handlers(bot)
    register_del_id_handlers(bot)
    register_view_ids_handlers(bot)
    register_restricted_operation_handlers(bot)
    register_unavailable_operation_handlers(bot)
    register_find_id_handlers(bot)
