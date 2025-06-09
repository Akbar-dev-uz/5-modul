from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.gnu_text_core import GNUTextCore
from routers.functions.funcs import get_locale

core = GNUTextCore(
    path="locales/{locale}/LC_MESSAGES",
    default_locale="en"
)

i18n = I18nMiddleware(core=core)
i18n.manager.locale_getter = get_locale
