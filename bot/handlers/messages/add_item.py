# mypy: disable-error-code="import-untyped"
from typing import Any
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from ..replies import (
    ADD_ITEM_MSG_START_SUCCESS,
    REJECT_MSG
)

def register_add_item_handlers(bot: AsyncTeleBot) -> None:
    @bot.message_handler(is_admin=True, state="default", text="Добавить вещь") # type: ignore[misc]
    async def handle_add_item_start_for_admins(msg: Message, data: dict[Any, Any]) -> None:
        await data["session"].clear_session()
        await data["session"].set_state("add_item:name")
        await bot.send_message(msg.chat.id, ADD_ITEM_MSG_START_SUCCESS)

    @bot.message_handler(is_admin=False, state="default", text="Добавить вещь") # type: ignore[misc]
    async def handle_add_item_start_for_users(msg: Message) -> None:
        await bot.send_message(msg.chat.id, REJECT_MSG)
