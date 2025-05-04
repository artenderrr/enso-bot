# mypy: disable-error-code="import-untyped"
from typing import Any
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from telebot.util import content_type_media
from ..replies import (
    REJECT_MSG,
    ADD_ITEM_MSG_START_SUCCESS,
    ADD_ITEM_MSG_NAME_FAILURE,
    ADD_ITEM_MSG_NAME_SUCCESS
)

def register_add_item_handlers(bot: AsyncTeleBot) -> None:
    @bot.message_handler(is_admin=True, state="default", text="Добавить вещь") # type: ignore[misc]
    async def handle_add_item_start_for_admins(msg: Message, data: dict[Any, Any]) -> None:
        await data["session"].clear_session()
        await data["session"].set_state("add_item:name")
        await bot.send_message(
            msg.chat.id, ADD_ITEM_MSG_START_SUCCESS, parse_mode="MarkdownV2"
        )

    @bot.message_handler(is_admin=False, state="default", text="Добавить вещь") # type: ignore[misc]
    async def handle_add_item_start_for_users(msg: Message) -> None:
        await bot.send_message(msg.chat.id, REJECT_MSG)

    @bot.message_handler(
        is_admin=True,
        state="add_item:name",
        content_types=content_type_media,
        func=lambda msg: True
    ) # type: ignore[misc]
    async def handle_add_item_name(msg: Message, data: dict[Any, Any]) -> None:
        if msg.content_type != "text" or len(msg.text) > 64:
            await bot.reply_to(
                msg, ADD_ITEM_MSG_NAME_FAILURE, parse_mode="MarkdownV2"
            )
        else:
            await data["session"].update_context(
                {"item_name": msg.text}
            )
            await data["session"].set_state("add_item:collection")
            await bot.send_message(
                msg.chat.id, ADD_ITEM_MSG_NAME_SUCCESS, parse_mode="MarkdownV2"
            )
