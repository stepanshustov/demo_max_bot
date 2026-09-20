import maxapi
import asyncio
import logging
from maxapi import Bot, Dispatcher
from maxapi.types import Message, MessageCreated, Command

from config import MAX_BOT_TOKEN
from routers import routers_list

logging.basicConfig(level=logging.INFO)

bot = Bot(token=MAX_BOT_TOKEN)
dp = Dispatcher()


async def main():
    for el in routers_list:
        dp.include_routers(el)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
