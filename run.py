import maxapi
import asyncio
import logging
from maxapi import Bot, Dispatcher
from maxapi.types import Message, MessageCreated, Command, BotCommand
# from maxapi.context import SimpleEventIsolation
from config import MAX_BOT_TOKEN
from routers import routers_list
from media import preload_media
from time import sleep

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"), # Пишем в файл
        logging.StreamHandler()                           # И выводим в консоль
    ]
)

bot = Bot(token=MAX_BOT_TOKEN)
dp = Dispatcher()


async def main():
    await preload_media(bot)
    for el in routers_list:
        dp.include_routers(el)
    await bot.set_commands(BotCommand(name="start", description="Главное меню"),
                           # BotCommand(name="help", description="Помощь"),
                           )
    await dp.start_polling(bot)


if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            print(e)
        sleep(3)
