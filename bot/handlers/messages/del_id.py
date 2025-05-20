# mypy: disable-error-code="import-untyped"
from typing import Any
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot
from ..replies import DEL_ID_MSG_START

def register_del_id_handlers(bot: AsyncTeleBot) -> None:
    @bot.message_handler(is_admin=True, state="default", text="Удалить номер") # type: ignore[misc]
    async def handle_del_id_start(msg: Message, data: dict[Any, Any]) -> None:
        await data["session"].clear_session()
        await data["session"].set_state("del_id:id")
        await bot.send_message(
            msg.chat.id, DEL_ID_MSG_START, parse_mode="MarkdownV2"
        )
