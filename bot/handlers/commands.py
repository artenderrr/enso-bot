# mypy: disable-error-code="import-untyped"
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from .utils.markup import get_admin_markup, get_user_markup
from .replies import START_CMD_REPLY

def register_command_handlers(bot: AsyncTeleBot) -> None:
    @bot.message_handler(is_admin=True, commands=["start"]) # type: ignore[misc]
    async def handle_start_command_for_admins(msg: Message) -> None:
        await bot.send_message(
            msg.chat.id,
            START_CMD_REPLY,
            parse_mode="MarkdownV2",
            reply_markup=get_admin_markup()
        )

    @bot.message_handler(commands=["start"]) # type: ignore[misc]
    async def handle_start_command_for_users(msg: Message) -> None:
        await bot.send_message(
            msg.chat.id,
            START_CMD_REPLY,
            parse_mode="MarkdownV2",
            reply_markup=get_user_markup()
        )
