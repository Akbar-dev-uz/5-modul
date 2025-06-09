from aiogram_i18n.cores.gnu_text_core import GNUTextCore
from aiogram_i18n import I18nMiddleware
from routers.functions.funcs import get_locale  # если ты определяешь язык сам

core = GNUTextCore(
    path="locales/{locale}/LC_MESSAGES",  # путь до твоих .mo/.po
    default_locale="en",
    domain="messages"
)

i18n = I18nMiddleware(
    core=core,
)
i18n.manager.locale_getter = get_locale  # если нужен кастомный выбор языка
