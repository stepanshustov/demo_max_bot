from pathlib import Path
from maxapi.types import InputMedia

from texts.carousel import NUMBERS_OF_TEXTS

MEDIA_DIR = Path(__file__).parent
_media_cache = {}


def get_media_carousel(number_page: int) -> InputMedia:
    """Просто возвращает объект из кэша. Бот здесь не нужен."""
    return _media_cache[number_page]


async def preload_media(bot) -> None:
    """Загружает все медиа в облако при старте. Принимает бота как аргумент."""
    pages = list(range(1, NUMBERS_OF_TEXTS + 1))

    for page in pages:
        path = str(MEDIA_DIR / "carousel" / f"page{page}.png")
        media = InputMedia(path=path)

        # Загружаем файл и получаем attachment объект
        attachment = await bot.upload_media(media)

        # Сохраняем attachment в кэш
        _media_cache[page] = attachment
        print(f"✅ Страница {page} загружена в кэш")