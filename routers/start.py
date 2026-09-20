from maxapi import F, Router
from maxapi.enums.format import Format
from maxapi.filters.command import CommandStart, Command
from maxapi.types import BotStarted, MessageCreated

from texts.hello import HELLO_TEXT
from keyboards import get_main_keyboard

router = Router(router_id="start")


@router.bot_started()
async def on_bot_started(event: BotStarted):
    """Event handler for bot started, before the command /start"""
    pass


@router.message_created(Command('start'))
async def start_command(event: MessageCreated):
    await event.message.answer(text=HELLO_TEXT, attachments=[await get_main_keyboard()])
