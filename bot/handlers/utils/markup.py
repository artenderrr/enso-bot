# mypy: disable-error-code="import-untyped"
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def create_markup_row(*args: str) -> list[KeyboardButton]:
    return [KeyboardButton(button_text) for button_text in args]

def get_admin_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for row in [
        create_markup_row("Добавить вещь", "Добавить номер"),
        create_markup_row("Удалить вещь", "Удалить номер"),
        create_markup_row("Список вещей", "Список номеров"),
        create_markup_row("Список отзывов")
    ]:
        markup.row(*row)
    return markup

def get_user_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Оставить отзыв"))
    return markup
