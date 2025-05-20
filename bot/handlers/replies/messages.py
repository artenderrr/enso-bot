from typing import Any
from .utils import escape_markdown

# general replies

REJECT_MSG = "❌"
REACTION_EMOJIS = ["\U0001F525", "\U0001F60E"]


# add_item replies

ADD_ID_MSG_START_FAILURE = "Прежде чем добавить номер, внесите в базу хотя бы одну вещь\\."
ADD_ITEM_MSG_START_SUCCESS = "Введите наименование вещи\\."
ADD_ITEM_MSG_NAME_FAILURE = (
    "Наименование вещи должно быть указано в виде текстового значения "
    "длиной не более 64 символов\\."
)
ADD_ITEM_MSG_NAME_SUCCESS = "Введите наименование коллекции\\."
ADD_ITEM_MSG_COLLECTION_FAILURE = (
    "Наименование коллекции должно быть указано в виде текстового значения "
    "длиной не более 64 символов\\."
)
ADD_ITEM_MSG_COLLECTION_SUCCESS = "Введите объем тиража в виде целого числа\\."
ADD_ITEM_MSG_VOLUME_FAILURE = (
    "Объем тиража должен быть указан как целое число больше нуля без дополнительных символов и "
    "длиной не более 9 цифр\\."
)
ADD_ITEM_MSG_VOLUME_SUCCESS = "Отправьте изображение вещи\\."
ADD_ITEM_MSG_IMAGE_FAILURE = "Отправьте изображение, а не что\\-либо другое\\."

def get_add_item_msg_image_success(
    item_id: int, item_name: str, item_collection: str, item_volume: int
) -> str:
    return (
        "Вещь была успешно добавлена\\!\n"
        "\n"
        f"• ID: *{item_id}*\n"
        f"• Наименование: *{escape_markdown(item_name)}*\n"
        f"• Коллекция: *{escape_markdown(item_collection)}*\n"
        f"• Тираж: *{item_volume:,} шт\\.*"
    )


# del_item replies

DEL_ITEM_MSG_START_SUCCESS = "Введите ID вещи, которую вы хотите удалить\\."
DEL_ITEM_MSG_ID_FORMAT_FAILURE = "ID должен быть указан как целое число без дополнительных символов\\."
DEL_ITEM_MSG_ID_LOOKUP_FAILURE = "Вещь с указанным ID не найдена\\. Может, это опечатка?"

def get_del_item_msg_id_success(item_name: str) -> str:
    return f"Вещь *{escape_markdown(item_name)}* была успешно удалена\\!"


# view_items replies

VIEW_ITEMS_MSG_FAILURE = "Вещей пока нет\\."

def get_view_items_msg_success(item_data: dict[str, Any]) -> str:
    return (
        f"• ID: *{item_data['id']}*\n"
        f"• Наименование: *{escape_markdown(item_data['name'])}*\n"
        f"• Коллекция: *{escape_markdown(item_data['collection'])}*\n"
        f"• Тираж: *{item_data['volume']:,} шт\\.*"
    )


# add_id replies

ADD_ID_MSG_START_SUCCESS = "Введите уникальный номер\\."
ADD_ID_MSG_ID_FORMAT_FAILURE = (
    "Уникальный номер должен состоять ровно из пяти цифр и не иметь в себе никаких других символов\\."
)
ADD_ID_MSG_ID_COLLISION_FAILURE = (
    "Этот уникальный номер уже занят\\."
)
ADD_ID_MSG_ID_SUCCESS = "Введите ID вещи, которую вы хотите привязать к номеру\\."
ADD_ID_MSG_ITEM_ID_FORMAT_FAILURE = "ID вещи должен быть указан как целое число без дополнительных символов\\."
ADD_ID_MSG_ITEM_ID_EXIST_FAILURE = "Вещи с таким ID не существует\\."
ADD_ID_MSG_ITEM_ID_SUCCESS = (
    "Введите имя или юзернейм владельца\\. Если указываете юзернейм, не забудьте добавить \"@\" в начале\\."
)
ADD_ID_MSG_OWNER_FAILURE = (
    "Имя или юзернейм владельца должны быть указаны в виде текстового значения длиной не более 64 символов\\."
)
ADD_ID_MSG_OWNER_SUCCESS = (
    "Введите дату покупки в формате ДД\\.ММ\\.ГГГГ или просто напишите \"сегодня\", \"вчера\" или \"позавчера\"\\."
)
ADD_ID_MSG_PURCHASE_DATE_FAILURE = (
    "Дата покупки должна быть указана в формате ДД\\.ММ\\.ГГГГ, "
    "либо как \"сегодня\", \"вчера\" или \"позавчера\"\\."
)
ADD_ID_MSG_PURCHASE_DATE_SUCCESS = (
    "Введите заметку, оставленную владельцем при покупке\\. Если владелец не оставил заметки, отправьте \"\\-\"\\."
)
ADD_ID_MSG_OWNER_NOTE_FORMAT_FAILURE = (
    "Заметка владельца должна быть указана в виде текстового значения длиной не более 64 символов\\."
)
ADD_ID_MSG_OWNER_NOTE_COLLISION_FAILURE = (
    "Ой, кажется, пока вы добавляли этот номер, кто\\-то из админов успел сделать это быстрее\\."
)

def get_add_id_msg_owner_note_success(
    id_: str,
    owner: str,
    item_name: str,
    item_collection: str,
    item_volume: int,
    purchase_date: str,
    owner_note: str | None
) -> str:
    owner_note_line = f"\n• Заметка владельца: *{escape_markdown(owner_note)}*" if owner_note else ""
    return (
        "Номер был успешно добавлен\\!\n"
        "\n"
        f"Уникальный номер _\\#{id_}_\n"
        "\n"
        f"• Владелец вещи: *{escape_markdown(owner)}*\n"
        f"• Наименование вещи: *{escape_markdown(item_name)}*\n"
        f"• Коллекция: *{escape_markdown(item_collection)}*\n"
        f"• Тираж: *{item_volume:,} шт\\.*\n"
        f"• Дата покупки: *{escape_markdown(purchase_date)}*\n"
        f"{owner_note_line}"
    )


# del_id replies

DEL_ID_MSG_START = "Введите уникальный номер, который вы хотите удалить\\."
DEL_ID_MSG_ID_FORMAT_FAILURE = (
    "Уникальный номер должен состоять ровно из пяти цифр и не иметь в себе никаких других символов\\."
)
DEL_ID_MSG_ID_LOOKUP_FAILURE = (
    "Этот номер отсутствует в базе\\."
)

def get_del_id_msg_id_success(id_: str) -> str:
    return f"Уникальный номер _\\#{id_}_ был успешно удален\\!"


# find_id replies

FIND_ID_MSG_FORMAT_FAILURE = (
    "Уникальный номер должен состоять ровно из пяти цифр "
    "и не иметь в себе никаких других символов\\."
)
FIND_ID_MSG_EXIST_FAILURE = (
    "Данные по этому номеру отсутствуют\\.\n"
    "\n"
    "Есть ошибка? @ensosupport"
)

def get_find_id_msg_success(
    id_: str,
    owner: str,
    item_name: str,
    item_collection: str,
    item_volume: int,
    purchase_date: str,
    owner_note: str | None
) -> str:
    owner_note_line = f"\n• Заметка владельца: *{escape_markdown(owner_note)}*\n" if owner_note else ""
    return (
        f"Уникальный номер _\\#{id_}_\n"
        "\n"
        f"• Владелец вещи: *{escape_markdown(owner)}*\n"
        f"• Наименование вещи: *{escape_markdown(item_name)}*\n"
        f"• Коллекция: *{escape_markdown(item_collection)}*\n"
        f"• Тираж: *{item_volume:,} шт\\.*\n"
        f"• Дата покупки: *{escape_markdown(purchase_date)}*\n"
        f"{owner_note_line}"
        "\n"
        "Есть ошибка? @ensosupport"
    )
