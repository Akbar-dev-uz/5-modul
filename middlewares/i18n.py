from aiogram.utils.i18n import I18n, I18nMiddleware
from aiogram.types import TelegramObject
from database.db import db
from os.path import join, dirname, abspath

BASE_DIR = abspath(join(dirname(__file__), ".."))
i18n = I18n(path=join(BASE_DIR, "locales"), default_locale="ru", domain="messages")


class CustomI18nMiddleware(I18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: dict) -> str:
        user = data.get("event_from_user")
        if user:
            user_lang = db.get_lang(user.id)
            if user_lang:
                return user_lang
        return self.i18n.default_locale


i18n_middleware = CustomI18nMiddleware(i18n)
