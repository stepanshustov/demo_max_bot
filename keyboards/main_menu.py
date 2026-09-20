from maxapi.types.attachments.buttons import CallbackButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder
from callbacks import MenuPayload
from maxapi.types.attachments.buttons.attachment_button import AttachmentButton


async def get_main_keyboard() -> AttachmentButton:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        CallbackButton(text="демо оставить заявку", payload=MenuPayload(action="form").pack())
    )
    keyboard.row(
        CallbackButton(text="демо карусель", payload=MenuPayload(action="carousel").pack())
    )
    keyboard.row(
        CallbackButton(text="демо FAQ", payload=MenuPayload(action="faq").pack())
    )
    return keyboard.as_markup()
