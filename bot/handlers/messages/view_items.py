# mypy: disable-error-code="import-untyped"
from typing import Any
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery
from telebot.util import content_type_media
from models import ClothingItem
from ..replies import VIEW_ITEMS_MSG_FAILURE, get_view_items_msg_success
from ..utils.markup import get_view_items_markup, remove_view_items_markup

def register_view_items_handlers(bot: AsyncTeleBot) -> None:
    @bot.message_handler(is_admin=True, state="default", text="Список вещей") # type: ignore[misc]
    async def handle_view_items_start(msg: Message, data: dict[Any, Any]) -> None:
        items = await ClothingItem.all()
        if not items:
            await bot.reply_to(msg, VIEW_ITEMS_MSG_FAILURE, parse_mode="MarkdownV2")
        else:
            await data["session"].clear_session()
            await data["session"].set_state("view_items")
            await data["session"].set_view_items_context(items)
            
            current_item = items[0]
            current_item_image = await current_item.load_image_bytes()
            
            item_viewer_message = await bot.send_photo(
                msg.chat.id,
                current_item_image,
                get_view_items_msg_success(current_item.__dict__),
                parse_mode="MarkdownV2",
                reply_markup=(get_view_items_markup() if len(items) > 1 else None)
            )
            await data["session"].update_context({
                "item_viewer_message_id": item_viewer_message.id
            })

    @bot.message_handler(
        is_admin=True,
        state="view_items",
        content_types=content_type_media,
        func=lambda msg: True
    ) # type: ignore[misc]
    async def handle_view_items_auto_quit(msg: Message, data: dict[Any, Any]) -> None:
        await remove_view_items_markup(bot, msg, data["session"])
        await data["session"].clear_session()
        await bot.process_new_messages([msg])

    @bot.callback_query_handler(callback=["view_items:backward", "view_items:forward"]) # type: ignore[misc]
    async def handle_view_items_navigation(
        call: CallbackQuery, data: dict[Any, Any]
    ) -> None:
        state = await data["session"].get_state()
        if state == "view_items":
            if call.data == "view_items:backward":
                await data["session"].decrement_current_view_item()
            elif call.data == "view_items:forward":
                await data["session"].increment_current_view_item()
            current_item_media = await data["session"].get_current_view_item_media()
            await bot.edit_message_media(
                current_item_media,
                call.message.chat.id,
                call.message.id,
                reply_markup=get_view_items_markup()
            )
        await bot.answer_callback_query(call.id)
