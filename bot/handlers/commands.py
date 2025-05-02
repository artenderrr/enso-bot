# mypy: disable-error-code="import-untyped"
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from .utils.markup import get_admin_markup, get_user_markup

def register_command_handlers(bot: AsyncTeleBot) -> None:
    @bot.message_handler(is_admin=True, commands=["start"]) # type: ignore[misc]
    async def handle_start_command_for_admins(msg: Message) -> None:
        await bot.send_message(
            msg.chat.id,
            "Hello, admin!",
            reply_markup=get_admin_markup()
        )

    @bot.message_handler(commands=["start"]) # type: ignore[misc]
    async def handle_start_command_for_users(msg: Message) -> None:
        await bot.send_message(
            msg.chat.id,
            "Hello, user!",
            reply_markup=get_user_markup()
        )
