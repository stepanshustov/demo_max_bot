from maxapi import Router, F
from maxapi.types import MessageCallback
from maxapi.context import MemoryContext, StatesGroup, State

from callbacks import MenuPayload, FaqPayload
from keyboards import get_faq_delete_keyboard, get_faq_list_keyboard
from texts.faq import FAQ_TEXTS

router = Router(router_id="faq")


@router.message_callback(MenuPayload.filter(F.action == "faq"))
async def faq(event: MessageCallback, payload: MenuPayload):
    if event.message is None:
        return
    await event.message.answer(
        text="Выберите вопрос", attachments=[await get_faq_list_keyboard()]
    )


@router.message_callback(FaqPayload.filter(F.number_question == -1))
async def faq_delete(event: MessageCallback, payload: FaqPayload):
    if event.message is None:
        return
    await event.message.delete()


@router.message_callback(FaqPayload.filter(F.number_question != -1))
async def faq_answer(event: MessageCallback, payload: FaqPayload):
    if event.message is None:
        return
    await event.message.answer(
        text=FAQ_TEXTS[payload.number_question]["answer"], attachments=[await get_faq_delete_keyboard()]
    )
