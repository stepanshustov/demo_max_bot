from maxapi import Router, F
from maxapi.types import MessageCallback
from maxapi.context import MemoryContext, StatesGroup, State

from texts.carousel import CAROUSEL_TEXTS, DEFAULT_PAGE, NUMBERS_OF_TEXTS
from callbacks import MenuPayload, CarouselPayload
from keyboards import get_carousel_keyboard

router = Router(router_id="carousel")


# Строка префикс перед текстом карточки
def help_number_page_func(n: int):
    return f"карточка: {n} из {NUMBERS_OF_TEXTS}\n"


@router.message_callback(MenuPayload.filter(F.action == "carousel"))
async def start_carousel(event: MessageCallback, payload: MenuPayload):
    if event.message is None:
        return
    print(payload.action)
    await event.message.answer(text=help_number_page_func(DEFAULT_PAGE) + CAROUSEL_TEXTS[DEFAULT_PAGE],
                               attachments=[await get_carousel_keyboard(DEFAULT_PAGE)])


@router.message_callback(CarouselPayload.filter())
async def main_carousel(event: MessageCallback, payload: CarouselPayload):
    if event.message is None:
        return
    print(payload.action)
    if payload.action == "to":
        await event.message.delete()
        await event.message.answer(text=help_number_page_func(payload.page) + CAROUSEL_TEXTS[payload.page],
                                   attachments=[await get_carousel_keyboard(payload.page)])
        return
    if payload.action == "select":
        await event.message.answer(text=f"Вы выбрали товар номер {payload.page}")
