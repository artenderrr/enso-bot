# mypy: disable-error-code="import-untyped"
from typing import Any
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot
from telebot.util import content_type_media
from models import ItemIdentifier, ClothingItem
from ..utils.date import is_valid_date_format, normalize_date
from ..replies import (
    ADD_ID_MSG_START_SUCCESS,
    ADD_ID_MSG_ID_FORMAT_FAILURE,
    ADD_ID_MSG_ID_COLLISION_FAILURE,
    ADD_ID_MSG_ID_SUCCESS,
    ADD_ID_MSG_ITEM_ID_FORMAT_FAILURE,
    ADD_ID_MSG_ITEM_ID_EXIST_FAILURE,
    ADD_ID_MSG_ITEM_ID_SUCCESS,
    ADD_ID_MSG_OWNER_FAILURE,
    ADD_ID_MSG_OWNER_SUCCESS,
    ADD_ID_MSG_PURCHASE_DATE_FAILURE,
    ADD_ID_MSG_PURCHASE_DATE_SUCCESS
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

    @bot.message_handler(
        is_admin=True,
        state="add_id:item_id",
        content_types=content_type_media,
        func=lambda msg: True
    ) # type: ignore[misc]
    async def handle_add_id_item_id(msg: Message, data: dict[Any, Any]) -> None:
        if msg.content_type != "text" or not msg.text.isdigit():
            await bot.reply_to(msg, ADD_ID_MSG_ITEM_ID_FORMAT_FAILURE, parse_mode="MarkdownV2")
        elif not await ClothingItem.exists(item_id := int(msg.text)):
            await bot.reply_to(msg, ADD_ID_MSG_ITEM_ID_EXIST_FAILURE, parse_mode="MarkdownV2")
        else:
            await data["session"].update_context({"id_item_id": item_id})
            await data["session"].set_state("add_id:owner")
            await bot.send_message(msg.chat.id, ADD_ID_MSG_ITEM_ID_SUCCESS, parse_mode="MarkdownV2")

    @bot.message_handler(
        is_admin=True,
        state="add_id:owner",
        content_types=content_type_media,
        func=lambda msg: True
    ) # type: ignore[misc]
    async def handle_add_id_owner(msg: Message, data: dict[Any, Any]) -> None:
        if msg.content_type != "text" or len(msg.text) > 64:
            await bot.reply_to(msg, ADD_ID_MSG_OWNER_FAILURE, parse_mode="MarkdownV2")
        else:
            owner = msg.text
            await data["session"].update_context({"id_owner": owner})
            await data["session"].set_state("add_id:purchase_date")
            await bot.send_message(msg.chat.id, ADD_ID_MSG_OWNER_SUCCESS, parse_mode="MarkdownV2")

    @bot.message_handler(
        is_admin=True,
        state="add_id:purchase_date",
        content_types=content_type_media,
        func=lambda msg: True
    ) # type: ignore[misc]
    async def handle_add_id_purchase_date(msg: Message, data: dict[Any, Any]) -> None:
        if (
            msg.content_type != "text" or
            not is_valid_date_format(provided_date := msg.text.strip().lower())
        ):
            await bot.reply_to(msg, ADD_ID_MSG_PURCHASE_DATE_FAILURE, parse_mode="MarkdownV2")
        else:
            purchase_date = normalize_date(provided_date)
            await data["session"].update_context({"id_purchase_date": purchase_date})
            await data["session"].set_state("add_id:owner_note")
            await bot.send_message(
                msg.chat.id, ADD_ID_MSG_PURCHASE_DATE_SUCCESS, parse_mode="MarkdownV2"
            )
