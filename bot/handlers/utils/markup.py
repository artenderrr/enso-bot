# mypy: disable-error-code="import-untyped"
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from models import UserSession

def create_markup_row(*args: str) -> list[KeyboardButton]:
    return [KeyboardButton(button_text) for button_text in args]

def get_admin_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for row in [
        create_markup_row("Добавить вещь", "Добавить номер"),
        create_markup_row("Удалить вещь", "Удалить номер"),
        create_markup_row("Список вещей", "Список номеров")
    ]:
        markup.row(*row)
    return markup

def get_user_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    # User buttons can be added like that:
    # markup.add(KeyboardButton("Какая-то кнопка"))
    return markup

def get_view_items_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("←", callback_data="view_items:backward"),
        InlineKeyboardButton("→", callback_data="view_items:forward")
    )
    return markup

async def remove_view_items_markup(
    bot: AsyncTeleBot, message: Message, session: UserSession
) -> None:
    context = await session.get_context()
    if context["items_count"] > 1:
        current_item_media = await session.get_current_view_item_media()
        await bot.edit_message_media(
            current_item_media,
            message.chat.id,
            context["item_viewer_message_id"],
            reply_markup=None
        )

def get_view_ids_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("←", callback_data="view_ids:backward"),
        InlineKeyboardButton("→", callback_data="view_ids:forward")
    )
    return markup

async def remove_view_ids_markup(
    bot: AsyncTeleBot, message: Message, session: UserSession
) -> None:
    from ..replies import get_view_ids_msg_success
    
    context = await session.get_context()
    if context["id_viewer_has_buttons"]:
        current_page_identifiers = await session.get_current_view_ids_page()
        await bot.edit_message_text(
            get_view_ids_msg_success(current_page_identifiers),
            message.chat.id,
            context["id_viewer_message_id"],
            parse_mode="MarkdownV2",
            reply_markup=None
        )
