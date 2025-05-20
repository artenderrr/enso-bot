# mypy: disable-error-code="import-untyped"
from typing import Any
from telebot.types import Message
from telebot.util import content_type_media
from telebot.async_telebot import AsyncTeleBot
from models import ItemIdentifier
from ..utils.markup import get_admin_markup
from ..replies import (
    DEL_ID_MSG_START,
    DEL_ID_MSG_ID_FORMAT_FAILURE,
    DEL_ID_MSG_ID_LOOKUP_FAILURE,
    get_del_id_msg_id_success
)

def register_del_id_handlers(bot: AsyncTeleBot) -> None:
    @bot.message_handler(is_admin=True, state="default", text="Удалить номер") # type: ignore[misc]
    async def handle_del_id_start(msg: Message, data: dict[Any, Any]) -> None:
        await data["session"].clear_session()
        await data["session"].set_state("del_id:id")
        await bot.send_message(
            msg.chat.id, DEL_ID_MSG_START, parse_mode="MarkdownV2"
        )

    @bot.message_handler(
        is_admin=True,
        state="del_id:id",
        content_types=content_type_media,
        func=lambda msg: True
    ) # type: ignore[misc]
    async def handle_del_id_id(msg: Message, data: dict[Any, Any]) -> None:
        if (
            msg.content_type != "text" or
            not msg.text.isdigit() or
            not len(msg.text) == 5
        ):
            await bot.reply_to(msg, DEL_ID_MSG_ID_FORMAT_FAILURE, parse_mode="MarkdownV2")
        else:
            identifier = await ItemIdentifier.get(msg.text)
            if not identifier:
                await bot.reply_to(
                    msg,
                    DEL_ID_MSG_ID_LOOKUP_FAILURE,
                    parse_mode="MarkdownV2"
                )
            else:
                await identifier.delete()
                await data["session"].clear_session()
                await bot.reply_to(
                    msg,
                    get_del_id_msg_id_success(identifier.id),
                    parse_mode="MarkdownV2",
                    reply_markup=get_admin_markup()
                )
