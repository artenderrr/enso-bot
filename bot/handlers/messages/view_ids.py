# mypy: disable-error-code="import-untyped"
from typing import Any
from telebot.util import content_type_media
from telebot.types import Message, CallbackQuery
from telebot.async_telebot import AsyncTeleBot
from core import config
from models import ItemIdentifier
from ..replies import VIEW_IDS_MSG_FAILURE, get_view_ids_msg_success
from ..utils.markup import get_view_ids_markup, remove_view_ids_markup

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
            
            id_viewer_message = await bot.send_message(
                msg.chat.id,
                get_view_ids_msg_success(current_page_identifiers),
                parse_mode="MarkdownV2",
                reply_markup=(
                    get_view_ids_markup()
                    if identifiers_count > config.view_ids_page_size
                    else None
                )
            )

            await data["session"].update_context({
                "id_viewer_message_id": id_viewer_message.id,
                "id_viewer_has_buttons": identifiers_count > config.view_ids_page_size
            })

    @bot.message_handler(
        is_admin=True,
        state="view_ids",
        content_types=content_type_media,
        func=lambda msg: True
    ) # type: ignore[misc]
    async def handle_view_ids_auto_quit(msg: Message, data: dict[Any, Any]) -> None:
        await remove_view_ids_markup(bot, msg, data["session"])
        await data["session"].clear_session()
        await bot.process_new_messages([msg])

    @bot.callback_query_handler(callback=["view_ids:backward", "view_ids:forward"]) # type: ignore[misc]
    async def handle_view_ids_navigation(
        call: CallbackQuery, data: dict[Any, Any]
    ) -> None:
        state = await data["session"].get_state()
        if state == "view_ids":
            if call.data == "view_ids:backward":
                await data["session"].decrement_current_view_ids_page()
            elif call.data == "view_ids:forward":
                await data["session"].increment_current_view_ids_page()
                
            identifiers_count = await ItemIdentifier.count()
            
            if identifiers_count == 0:
                await bot.edit_message_text(
                    VIEW_IDS_MSG_FAILURE,
                    call.message.chat.id,
                    call.message.id,
                    parse_mode="MarkdownV2"
                )
            else:
                current_page_identifiers = await data["session"].get_current_view_ids_page()
                await bot.edit_message_text(
                    get_view_ids_msg_success(current_page_identifiers),
                    call.message.chat.id,
                    call.message.id,
                    parse_mode="MarkdownV2",
                    reply_markup=(
                        get_view_ids_markup()
                        if identifiers_count > config.view_ids_page_size
                        else None
                    )
                )
        await bot.answer_callback_query(call.id)
