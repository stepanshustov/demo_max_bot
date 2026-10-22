from functools import wraps
from cachetools import TTLCache
from dataclasses import fields, is_dataclass
from typing import Any


class CallbackDedup:
    """Универсальный декоратор для дедупликации callback-действий.

    Кэширует комбинацию (message_id, параметры_действия), чтобы не выполнять
    одно и то же действие несколько раз для одного сообщения.
    Работает для любых кнопок и payload-типов.
    """

    def __init__(self, ttl: int | float = 30, maxsize: int = 1000):
        self._cache = TTLCache(maxsize=maxsize, ttl=ttl)

    def _extract_payload_params(self, payload: Any) -> tuple:
        """Извлекает все значимые параметры из payload для формирования ключа."""
        if payload is None:
            return ()

        # Если payload - это dataclass (как в maxapi), извлекаем все поля
        if is_dataclass(payload) and not isinstance(payload, type):
            return tuple(getattr(payload, field.name) for field in fields(payload))

        # Если payload - это dict
        if isinstance(payload, dict):
            return tuple(sorted(payload.items()))

        # Если payload - это объект с атрибутами
        if hasattr(payload, '__dict__'):
            return tuple(sorted(
                (k, v) for k, v in payload.__dict__.items()
                if not k.startswith('_')
            ))

        # Иначе просто преобразуем в строку
        return (str(payload),)

    def __call__(self, func):
        @wraps(func)
        async def wrapper(event, *args, **kwargs):
            # Извлекаем message_id
            message_id = None
            if hasattr(event, 'message') and event.message is not None:
                # В maxapi ID сообщения лежит в event.message.body.mid
                if hasattr(event.message, 'body') and hasattr(event.message.body, 'mid'):
                    message_id = event.message.body.mid
                elif hasattr(event.message, 'mid'):
                    message_id = event.message.mid

            # Извлекаем payload (может быть в kwargs или в args)
            payload = kwargs.get('payload')
            if payload is None and len(args) > 1:
                payload = args[1]  # Обычно payload идет вторым аргументом после event

            if message_id is not None and payload is not None:
                # Формируем ключ: (message_id, все_параметры_действия)
                params = self._extract_payload_params(payload)
                cache_key = (message_id, params)

                if cache_key in self._cache:
                    # Уже выполняли это действие для этого сообщения — игнорируем
                    await event.answer()
                    return None

                # Запоминаем, что начали выполнять
                self._cache[cache_key] = True

            return await func(event, *args, **kwargs)

        return wrapper
