from maxapi.types.attachments.buttons import CallbackButton
from maxapi.types.attachments.buttons.attachment_button import AttachmentButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

from callbacks import FaqPayload
from texts.faq import FAQ_TEXTS


async def get_faq_list_keyboard() -> AttachmentButton:
    keyboard = InlineKeyboardBuilder()
    for i in FAQ_TEXTS.keys():
        keyboard.row(
            CallbackButton(text=FAQ_TEXTS[i]["question"], payload=FaqPayload(number_question=i).pack())
        )
    return keyboard.as_markup()


async def get_faq_delete_keyboard() -> AttachmentButton:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        CallbackButton(text="Очистить", payload=FaqPayload(number_question=-1).pack())
    )
    return keyboard.as_markup()
