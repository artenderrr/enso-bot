# mypy: disable-error-code="import-untyped"
from telebot.types import Message
from telebot.util import content_type_media
from telebot.async_telebot import AsyncTeleBot
from models import ClothingItem, ItemIdentifier
from ..replies import (
    FIND_ID_MSG_FORMAT_FAILURE,
    FIND_ID_MSG_EXIST_FAILURE,
    get_find_id_msg_success
)

def register_find_id_handlers(bot: AsyncTeleBot) -> None:
    @bot.message_handler(
        state="default",
        content_types=content_type_media,
        func=lambda msg: True
    ) # type: ignore[misc]
    async def handle_find_id(msg: Message) -> None:
        if (
            msg.content_type != "text" or
            not msg.text.isdigit() or
            not len(msg.text) == 5
        ):
            await bot.reply_to(msg, FIND_ID_MSG_FORMAT_FAILURE, parse_mode="MarkdownV2")
        else:
            identifier = await ItemIdentifier.get(msg.text)
            if not identifier:
                await bot.reply_to(
                    msg, FIND_ID_MSG_EXIST_FAILURE, parse_mode="MarkdownV2"
                )
            else:
                item = await ClothingItem.get(identifier.item_id)
                item_image = await item.load_image_bytes()
                await bot.send_photo(
                    msg.chat.id,
                    item_image,
                    get_find_id_msg_success(
                        identifier.id,
                        identifier.owner,
                        item.name,
                        item.collection,
                        item.volume,
                        identifier.purchase_date,
                        identifier.owner_note
                    ),
                    parse_mode="MarkdownV2"
                )
