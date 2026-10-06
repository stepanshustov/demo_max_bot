from functools import wraps
from cachetools import LRUCache
from typing import Callable, Any


class CallbackDedup:
    """Класс-декоратор для дедупликации callback'ов."""

    def __init__(self, maxsize: int = 1000):
        # Каждый экземпляр класса имеет свой изолированный кэш
        self._cache = LRUCache(maxsize=maxsize)

    def __call__(self, func: Callable) -> Callable:
        """Делает экземпляр класса декоратором."""

        @wraps(func)
        async def wrapper(event, *args, **kwargs):
            # Проверяем, есть ли callback_id
            if hasattr(event, 'callback') and hasattr(event.callback, 'callback_id'):
                cb_id = event.callback.callback_id

                # Если уже обрабатывали — снимаем часики и выходим
                if cb_id in self._cache:
                    await event.answer(show_alert=False)
                    return None

                # Запоминаем
                self._cache[cb_id] = True

            # Вызываем оригинальную функцию
            return await func(event, *args, **kwargs)

        return wrapper

    def clear(self):
        """Метод для очистки кэша (например, при тестировании или перезапуске)."""
        self._cache.clear()

    @property
    def size(self) -> int:
        """Текущий размер кэша (для мониторинга/отладки)."""
        return len(self._cache)