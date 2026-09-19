from maxapi import F, Router
from maxapi.enums.format import Format
from maxapi.filters.command import CommandStart, Command
from maxapi.types import BotStarted, MessageCreated


from texts import HELLO_TEXT


router = Router(router_id="start")

@router.bot_started()
async def on_bot_started(event: BotStarted):
    """Event handler for bot started, before the command /start"""
    pass

@router.message_created(CommandStart)
async def start_command(event: MessageCreated):
    await event.message.answer(HELLO_TEXT.text)

