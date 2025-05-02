# mypy: disable-error-code="import-untyped"
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

def register_command_handlers(bot: AsyncTeleBot) -> None:
    @bot.message_handler(commands=["start"]) # type: ignore[misc]
    async def handle_start_command(msg: Message) -> None:
        await bot.send_message(msg.chat.id, "Let's start!")
