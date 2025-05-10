# mypy: disable-error-code="import-untyped"
from typing import Any
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot
from ..replies import ADD_ID_MSG_START_SUCCESS

def register_add_id_handlers(bot: AsyncTeleBot) -> None:
    @bot.message_handler(is_admin=True, state="default", text="Добавить номер") # type: ignore[misc]
    async def handle_add_id_start(msg: Message, data: dict[Any, Any]) -> None:
        await data["session"].clear_session()
        await data["session"].set_state("add_id:id")
        await bot.send_message(
            msg.chat.id, ADD_ID_MSG_START_SUCCESS, parse_mode="MarkdownV2"
        )
