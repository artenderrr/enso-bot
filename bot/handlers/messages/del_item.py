# mypy: disable-error-code="import-untyped"
from typing import Any
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot
from telebot.util import content_type_media
from models import ClothingItem
from ..replies import (
    DEL_ITEM_MSG_START_SUCCESS,
    DEL_ITEM_MSG_ID_FORMAT_FAILURE,
    DEL_ITEM_MSG_ID_LOOKUP_FAILURE,
    get_del_item_msg_id_success
)
from ..utils.markup import get_admin_markup

def register_del_item_handlers(bot: AsyncTeleBot) -> None:
    @bot.message_handler(is_admin=True, state="default", text="Удалить вещь") # type: ignore[misc]
    async def handle_del_item_start(msg: Message, data: dict[Any, Any]) -> None:
        await data["session"].clear_session()
        await data["session"].set_state("del_item:id")
        await bot.send_message(
            msg.chat.id, DEL_ITEM_MSG_START_SUCCESS, parse_mode="MarkdownV2"
        )

    @bot.message_handler(
        is_admin=True,
        state="del_item:id",
        content_types=content_type_media,
        func=lambda msg: True
    ) # type: ignore[misc]
    async def handle_del_item_id(msg: Message, data: dict[Any, Any]) -> None:
        if msg.content_type != "text" or not msg.text.isdigit():
            await bot.reply_to(
                msg,
                DEL_ITEM_MSG_ID_FORMAT_FAILURE,
                parse_mode="MarkdownV2"
            )
        else:
            item_id = int(msg.text)
            item = await ClothingItem.get(item_id)
            if not item:
                await bot.reply_to(
                    msg,
                    DEL_ITEM_MSG_ID_LOOKUP_FAILURE,
                    parse_mode="MarkdownV2"
                )
            else:
                await item.delete()
                await data["session"].clear_session()
                await bot.reply_to(
                    msg,
                    get_del_item_msg_id_success(item.name),
                    parse_mode="MarkdownV2",
                    reply_markup=get_admin_markup()
                )
