# mypy: disable-error-code="import-untyped"
from typing import Any
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot

async def delete_item_viewer_message(
    bot: AsyncTeleBot, msg: Message, data: dict[Any, Any]
) -> None:
    state = await data["session"].get_state()
    if state == "view_items":
        context = await data["session"].get_context()
        await bot.delete_message(msg.chat.id, context["item_viewer_message_id"])
