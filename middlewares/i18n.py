from aiogram_i18n import I18nMiddleware
from routers.functions.funcs import get_locale


i18n = I18nMiddleware(
    path="locales",
    default_locale="en",
    domain="messages",
    get_locale=get_locale,
)