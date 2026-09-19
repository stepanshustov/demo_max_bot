from maxapi.filters.callback_payload import CallbackPayload


class MenuPayload(CallbackPayload, prefix="menu"):
    """Buttons for main menu"""
    action: str  # form | catalog | faq | about
