from maxapi.filters.callback_payload import CallbackPayload


class MenuPayload(CallbackPayload, prefix="menu"):
    """Кнопки для главного меню"""
    action: str  # form | catalog | faq | about


class CarouselPayload(CallbackPayload, prefix="carousel"):
    """Кнопки для карусели, хранит номер карточки к кторой нужно перейти или выбрать"""
    action: str # to | select
    page: int
