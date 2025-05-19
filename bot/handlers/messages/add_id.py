# mypy: disable-error-code="import-untyped"
from typing import Any
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot
from telebot.util import content_type_media
from models import ItemIdentifier, ClothingItem
from ..utils.markup import get_admin_markup
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
    ADD_ID_MSG_PURCHASE_DATE_SUCCESS,
    ADD_ID_MSG_OWNER_NOTE_FORMAT_FAILURE,
    ADD_ID_MSG_OWNER_NOTE_COLLISION_FAILURE,
    get_add_id_msg_owner_note_success
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

    @bot.message_handler(
        is_admin=True,
        state="add_id:owner_note",
        content_types=content_type_media,
        func=lambda msg: True
    ) # type: ignore[misc]
    async def handle_add_id_owner_note(msg: Message, data: dict[Any, Any]) -> None:
        if msg.content_type != "text" or len(msg.text) > 64:
            await bot.reply_to(msg, ADD_ID_MSG_OWNER_NOTE_FORMAT_FAILURE, parse_mode="MarkdownV2")
        else:
            owner_note = msg.text if msg.text != "-" else None
            await data["session"].update_context({"id_owner_note": owner_note})
            context = await data["session"].get_context()
            
            if await ItemIdentifier.exists(context["id_id"]):
                await data["session"].clear_session()
                await bot.send_message(
                    msg.chat.id, ADD_ID_MSG_OWNER_NOTE_COLLISION_FAILURE, parse_mode="MarkdownV2"
                )
            else:
                identifier = await ItemIdentifier.create(
                    context["id_id"],
                    context["id_item_id"],
                    context["id_owner"],
                    context["id_purchase_date"],
                    context["id_owner_note"],
                )
                item = await ClothingItem.get(identifier.item_id)
                item_image = await item.load_image_bytes()
                
                await data["session"].clear_session()

                await bot.send_photo(
                    msg.chat.id,
                    item_image,
                    get_add_id_msg_owner_note_success(
                        identifier.id,
                        identifier.owner,
                        item.name,
                        item.collection,
                        item.volume,
                        identifier.purchase_date,
                        identifier.owner_note
                    ),
                    parse_mode="MarkdownV2",
                    reply_markup=get_admin_markup()
                )
