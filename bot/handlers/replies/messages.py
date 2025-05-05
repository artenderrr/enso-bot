REJECT_MSG = "❌"

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
    "Объем тиража должен быть указан как целое число без дополнительных символов "
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
        f"• Наименование: *{item_name}*\n"
        f"• Коллекция: *{item_collection}*\n"
        f"• Тираж: *{item_volume:,} шт\\.*"
    )

REACTION_EMOJIS = ["\U0001F525", "\U0001F60E"]
