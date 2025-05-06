# mypy: disable-error-code="import-untyped"
from typing import Any
import random
from pathlib import Path
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, ReactionTypeEmoji
from telebot.util import content_type_media
from models import ClothingItem
from ..replies import (
    ADD_ITEM_MSG_START_SUCCESS,
    ADD_ITEM_MSG_NAME_FAILURE,
    ADD_ITEM_MSG_NAME_SUCCESS,
    ADD_ITEM_MSG_COLLECTION_FAILURE,
    ADD_ITEM_MSG_COLLECTION_SUCCESS,
    ADD_ITEM_MSG_VOLUME_FAILURE,
    ADD_ITEM_MSG_VOLUME_SUCCESS,
    ADD_ITEM_MSG_IMAGE_FAILURE,
    get_add_item_msg_image_success,
    REACTION_EMOJIS
)
from ..utils.markup import get_admin_markup

def register_add_item_handlers(bot: AsyncTeleBot) -> None:
    @bot.message_handler(is_admin=True, state="default", text="Добавить вещь") # type: ignore[misc]
    async def handle_add_item_start(msg: Message, data: dict[Any, Any]) -> None:
        await data["session"].clear_session()
        await data["session"].set_state("add_item:name")
        await bot.send_message(
            msg.chat.id, ADD_ITEM_MSG_START_SUCCESS, parse_mode="MarkdownV2"
        )

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

    @bot.message_handler(
        is_admin=True,
        state="add_item:collection",
        content_types=content_type_media,
        func=lambda msg: True
    ) # type: ignore[misc]
    async def handle_add_item_collection(msg: Message, data: dict[Any, Any]) -> None:
        if msg.content_type != "text" or len(msg.text) > 64:
            await bot.reply_to(
                msg, ADD_ITEM_MSG_COLLECTION_FAILURE, parse_mode="MarkdownV2"
            )
        else:
            await data["session"].update_context(
                {"item_collection": msg.text}
            )
            await data["session"].set_state("add_item:volume")
            await bot.send_message(
                msg.chat.id, ADD_ITEM_MSG_COLLECTION_SUCCESS, parse_mode="MarkdownV2"
            )

    @bot.message_handler(
        is_admin=True,
        state="add_item:volume",
        content_types=content_type_media,
        func=lambda msg: True
    ) # type: ignore[misc]
    async def handle_add_item_volume(msg: Message, data: dict[Any, Any]) -> None:
        if msg.content_type != "text" or not msg.text.isdigit() or len(msg.text) > 9:
            await bot.reply_to(
                msg, ADD_ITEM_MSG_VOLUME_FAILURE, parse_mode="MarkdownV2"
            )
        else:
            await data["session"].update_context(
                {"item_volume": int(msg.text)}
            )
            await data["session"].set_state("add_item:image")
            await bot.send_message(
                msg.chat.id, ADD_ITEM_MSG_VOLUME_SUCCESS, parse_mode="MarkdownV2"
            )

    @bot.message_handler(
        is_admin=True,
        state="add_item:image",
        content_types=content_type_media,
        func=lambda msg: True
    ) # type: ignore[misc]
    async def handle_add_item_image(msg: Message, data: dict[Any, Any]) -> None:
        if msg.content_type != "photo":
            await bot.reply_to(
                msg, ADD_ITEM_MSG_IMAGE_FAILURE, parse_mode="MarkdownV2"
            )
        else:
            await bot.set_message_reaction(
                msg.chat.id,
                msg.id,
                [ReactionTypeEmoji(random.choice(REACTION_EMOJIS))],
                is_big=False
            )
        
            context = await data["session"].get_context()
            image = await bot.get_file(file_id=msg.photo[-1].file_id)
            image_extension = Path(image.file_path).suffix
            image_bytes = await bot.download_file(image.file_path)
            
            item = await ClothingItem.create(
                name=context["item_name"],
                collection=context["item_collection"],
                volume=context["item_volume"],
                image_bytes=image_bytes,
                image_extension=image_extension
            )

            await data["session"].clear_session()

            await bot.send_photo(
                msg.chat.id,
                image_bytes,
                get_add_item_msg_image_success(
                    item.id,
                    item.name,
                    item.collection,
                    item.volume
                ),
                parse_mode="MarkdownV2",
                reply_markup=get_admin_markup()
            )
