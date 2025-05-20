# mypy: disable-error-code="import-untyped"
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot
from ..replies import REJECT_MSG

RESTRICTED_OPERATIONS = [
    "Добавить вещь",
    "Удалить вещь",
    "Список вещей",
    "Добавить номер",
    "Удалить номер",
    "Список номеров",
    "Список отзывов"
]

def register_restricted_operation_handlers(bot: AsyncTeleBot) -> None:
    @bot.message_handler(
        is_admin=False, state="default", text=RESTRICTED_OPERATIONS
    ) # type: ignore[misc]
    async def handle_restricted_operations(msg: Message) -> None:
        await bot.send_message(
            msg.chat.id, REJECT_MSG, parse_mode="MarkdownV2"
        )
