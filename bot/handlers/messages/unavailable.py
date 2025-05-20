# mypy: disable-error-code="import-untyped"
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot
from ..replies import UNAVAILABLE_MSG

UNAVAILABLE_OPERATIONS = [
    "Список номеров",
    "Оставить отзыв",
    "Список отзывов"
]

def register_unavailable_operation_handlers(bot: AsyncTeleBot) -> None:
    @bot.message_handler(state="default", text=UNAVAILABLE_OPERATIONS) # type: ignore[misc]
    async def handle_unavailable_operations(msg: Message) -> None:
        await bot.reply_to(
            msg, UNAVAILABLE_MSG, parse_mode="MarkdownV2"
        )
