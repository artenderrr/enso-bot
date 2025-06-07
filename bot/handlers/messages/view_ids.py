# mypy: disable-error-code="import-untyped"
from typing import Any
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot
from core import config
from models import ItemIdentifier
from ..replies import VIEW_IDS_MSG_FAILURE, get_view_ids_msg_success
from ..utils.markup import get_view_ids_markup

def register_view_ids_handlers(bot: AsyncTeleBot) -> None:
    @bot.message_handler(is_admin=True, state="default", text="Список номеров") # type: ignore[misc]
    async def handle_view_ids_start(msg: Message, data: dict[Any, Any]) -> None:
        identifiers_count = await ItemIdentifier.count()
        if identifiers_count == 0:
            await bot.reply_to(msg, VIEW_IDS_MSG_FAILURE, parse_mode="MarkdownV2")
        else:
            await data["session"].clear_session()
            await data["session"].set_state("view_ids")
            await data["session"].update_context({"current_view_ids_page": 1})
            
            current_page_identifiers = await data["session"].get_current_view_ids_page()
            
            await bot.send_message(
                msg.chat.id,
                get_view_ids_msg_success(current_page_identifiers),
                parse_mode="MarkdownV2",
                reply_markup=(
                    get_view_ids_markup()
                    if identifiers_count > config.view_ids_page_size
                    else None
                )
            )
