import time
from typing import Any, Awaitable, Callable, Dict
from maxapi.filters.middleware import BaseMiddleware
from maxapi.types import UpdateUnion
import re
import phonenumbers

# Разрешены буквы, пробел и дефис. От 2 до 64 символов.
_NAME_RE = re.compile(r"^[А-Яа-яЁёA-Za-z][А-Яа-яЁёA-Za-z\-\s]{1,63}$")


def validate_name(value: str) -> str:
    """Возвращает имя с заглавными буквами или кидает ValueError."""
    value = value.strip()
    if not _NAME_RE.match(value):
        raise ValueError("Имя должно содержать только буквы, пробел или дефис.")
    return " ".join(word.capitalize() for word in value.split())


def validate_phone(value: str, region: str = "RU") -> str:
    """Возвращает номер в формате E.164 (+7999...) или кидает ValueError."""
    try:
        num = phonenumbers.parse(value, region)
    except phonenumbers.NumberParseException as exc:
        raise ValueError("Не могу разобрать номер.") from exc

    if not phonenumbers.is_valid_number(num):
        raise ValueError("Номер недействителен.")

    return phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.E164)


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 1.0):
        self.rate_limit = rate_limit  # Секунд между запросами
        self.user_cache: Dict[int, float] = {}

    async def __call__(
            self,
            handler: Callable[[UpdateUnion, Dict[str, Any]], Awaitable[Any]],
            event: UpdateUnion,
            data: Dict[str, Any],
    ) -> Any:
        # Получаем ID пользователя и чата (как в FSM-контексте)
        chat_id, user_id = event.get_ids()

        if user_id:
            now = time.time()
            last_time = self.user_cache.get(user_id, 0.0)

            # Если с прошлого сообщения прошло меньше rate_limit секунд — блокируем
            if now - last_time < self.rate_limit:
                return None  # Молча игнорируем (или можно отправить предупреждение)

            self.user_cache[user_id] = now

        return await handler(event, data)
