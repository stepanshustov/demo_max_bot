from maxapi.types.attachments.buttons import CallbackButton
from maxapi.types.attachments.buttons.attachment_button import AttachmentButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

from callbacks import CarouselPayload
from texts.carousel import NUMBERS_OF_TEXTS


def get_numbers_of_texts(n: int) -> int:
    n = n % NUMBERS_OF_TEXTS
    if n == 0:
        n = NUMBERS_OF_TEXTS
    return n


async def get_carousel_keyboard(number_page: int) -> AttachmentButton:
    """Создает клавиатуру с кнопками навигации по карточкам."""
    # print("ffffffffffff")
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        CallbackButton(
            text="️Назад",
            payload=CarouselPayload(
                action="to", page=get_numbers_of_texts(number_page - 1)).pack(),
        ),
        CallbackButton(
            text="Вперёд",
            payload=CarouselPayload(
                action="to", page=get_numbers_of_texts(number_page + 1)).pack(),
        )
    )
    keyboard.row(
        CallbackButton(
            text="Выбрать",
            payload=CarouselPayload(
                action="select", page=number_page).pack(),
        )
    )
    return keyboard.as_markup()
