from typing import Any

START_CMD_REPLY = (
    "SUp\\! Я ЕНСИК :S"
    "\n\n"
    "Я инструмент для проверки и поиска владельца вещи по ее "
    "*уникальному номеру* в общей базе обладателей вещей магазина\\."
    "\n\n"
    "Отправь мне *пятизначный номер* с головной бирки вещи и я "
    "сообщу тебе данные о владельце, которые были оставлены при "
    "*оформлении заказа*\\."
    "\n\n"
    "Вопросы/cвязь: @ensosupport"
)

CANCEL_CMD_REPLY_FAILURE = (
    "Сейчас нет активной операции, которую можно было бы отменить."
)
CANCEL_CMD_REPLY_SUCCESS = "Операция была отменена."

def get_debug_cmd_reply(debug_data: dict[str, Any]) -> str:
    return "\n".join(f"*{k}*: `{v}`" for k, v in debug_data.items())
