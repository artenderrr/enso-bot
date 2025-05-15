# mypy: disable-error-code="import-untyped"
from typing import Any
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot
from telebot.util import content_type_media
from models import ItemIdentifier
from ..replies import (
    ADD_ID_MSG_START_SUCCESS,
    ADD_ID_MSG_ID_FORMAT_FAILURE,
    ADD_ID_MSG_ID_COLLISION_FAILURE,
    ADD_ID_MSG_ID_SUCCESS
)

def register_add_id_handlers(bot: AsyncTeleBot) -> None:
    @bot.message_handler(is_admin=True, state="default", text="Добавить номер") # type: ignore[misc]
    async def handle_add_id_start(msg: Message, data: dict[Any, Any]) -> None:
        await data["session"].clear_session()
        await data["session"].set_state("add_id:id")
        await bot.send_message(
            msg.chat.id, ADD_ID_MSG_START_SUCCESS, parse_mode="MarkdownV2"
        )

    @bot.message_handler(
        is_admin=True,
        state="add_id:id",
        content_types=content_type_media,
        func=lambda msg: True
    ) # type: ignore[misc]
    async def handle_add_id_id(msg: Message, data: dict[Any, Any]) -> None:
        if (
            msg.content_type != "text" or
            not msg.text.isdigit() or
            len(msg.text) != 5
        ):
            await bot.reply_to(msg, ADD_ID_MSG_ID_FORMAT_FAILURE, parse_mode="MarkdownV2")
        elif await ItemIdentifier.exists(msg.text):
            await bot.reply_to(msg, ADD_ID_MSG_ID_COLLISION_FAILURE, parse_mode="MarkdownV2")
        else:
            id_ = msg.text.strip()
            await data["session"].update_context({"id_id": id_})
            await data["session"].set_state("add_id:item_id")
            await bot.send_message(msg.chat.id, ADD_ID_MSG_ID_SUCCESS, parse_mode="MarkdownV2")
