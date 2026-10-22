from maxapi import Router, F
from maxapi.context import MemoryContext, State, StatesGroup
from maxapi.types import MessageCreated, MessageCallback

from utils import validate_name, validate_phone
from callbacks import MenuPayload
from utils import ThrottlingMiddleware


class Form(StatesGroup):
    waiting_name = State()
    waiting_phone = State()


router = Router(router_id="form")


@router.message_callback(MenuPayload.filter(F.action == "form"), ThrottlingMiddleware(5))
async def start_form_button(event: MessageCallback, context: MemoryContext, payload: MenuPayload):
    await event.answer()
    await context.set_state(Form.waiting_name)
    await event.message.answer("Введите ваше имя:")


@router.message_created(Form.waiting_name, ThrottlingMiddleware(2))
async def process_name(event: MessageCreated, context: MemoryContext):
    try:
        name = validate_name(event.message.body.text)
    except ValueError as err:
        await event.message.answer(f"{err}\nПопробуйте ещё раз.")
        return

    await context.update_data(name=name)
    await context.set_state(Form.waiting_phone)
    await event.message.answer(f"Приятно познакомиться, {name}!\nОтправьте номер телефона:")


@router.message_created(Form.waiting_phone, ThrottlingMiddleware(2))
async def process_phone(event: MessageCreated, context: MemoryContext):
    try:
        phone = validate_phone(event.message.body.text)
    except ValueError as err:
        await event.message.answer(f"{err}\nПопробуйте ещё раз.")
        return

    await context.update_data(phone=phone)
    data = await context.get_data()

    await context.set_state(None)
    await event.message.answer(f"Администратор получит заявку:!\nИмя: {data['name']}\nТелефон: {data['phone']}")
