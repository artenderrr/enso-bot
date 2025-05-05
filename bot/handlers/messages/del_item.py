# mypy: disable-error-code="import-untyped"
from typing import Any
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot
from ..replies import (
    DEL_ITEM_MSG_START_SUCCESS
)

def register_del_item_handlers(bot: AsyncTeleBot) -> None:
    @bot.message_handler(is_admin=True, state="default", text="Удалить вещь") # type: ignore[misc]
    async def handle_del_item_start_for_admins(msg: Message, data: dict[Any, Any]) -> None:
        await data["session"].clear_session()
        await data["session"].set_state("del_item:id")
        await bot.send_message(
            msg.chat.id, DEL_ITEM_MSG_START_SUCCESS, parse_mode="MarkdownV2"
        )
