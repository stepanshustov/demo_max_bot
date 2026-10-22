from maxapi import Router, F
from maxapi.types import MessageCallback
from maxapi.context import MemoryContext, StatesGroup, State

from texts.carousel import CAROUSEL_TEXTS, DEFAULT_PAGE, NUMBERS_OF_TEXTS
from callbacks import MenuPayload, CarouselPayload
from keyboards import get_carousel_keyboard
from media import get_media_carousel
from utils import CallbackDedup

router = Router(router_id="carousel")

dedup = CallbackDedup(ttl=2)
dedup_to = CallbackDedup(ttl=0.2)

# Строка префикс перед текстом карточки
def help_number_page_func(n: int):
    return f"карточка: {n} из {NUMBERS_OF_TEXTS}\n"


@router.message_callback(MenuPayload.filter(F.action == "carousel"))
@dedup
async def start_carousel(event: MessageCallback, payload: MenuPayload):
    if event.message is None:
        return
    # print(payload.action
    media = get_media_carousel(DEFAULT_PAGE)
    await event.message.answer(text=help_number_page_func(DEFAULT_PAGE) + CAROUSEL_TEXTS[DEFAULT_PAGE],
                               attachments=[media, await get_carousel_keyboard(DEFAULT_PAGE)])


@router.message_callback(CarouselPayload.filter(F.action == "to"))
@dedup_to
async def main_carousel_to(event: MessageCallback, payload: CarouselPayload):
    if event.message is None:
        return
    # print(payload.action)
    media = get_media_carousel(payload.page)
    # await event.message.delete()
    await event.message.edit(text=help_number_page_func(payload.page) + CAROUSEL_TEXTS[payload.page],
                             attachments=[media, await get_carousel_keyboard(payload.page)])



@router.message_callback(CarouselPayload.filter(F.action == "select"))
@dedup
async def main_carousel_select(event: MessageCallback, payload: CarouselPayload):
    if event.message is None:
        return
    if payload.action == "select":
        await event.message.answer(text=f"Вы выбрали товар номер {payload.page}")
