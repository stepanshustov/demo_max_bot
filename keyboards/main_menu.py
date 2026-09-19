from maxapi.types.attachments.buttons import CallbackButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

from calbacks import MenuPayload


async def get_main_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        CallbackButton(text="демо оставить заявку", payload=MenuPayload(action="form").pack())
    )
    return keyboard.as_markup()