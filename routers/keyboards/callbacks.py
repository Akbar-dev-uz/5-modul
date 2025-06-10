from enum import Enum

from aiogram.filters.callback_data import CallbackData


class Languages(Enum):
    UZ = "uz"
    RU = "ru"
    EN = "en"


class Language(CallbackData, prefix='lang'):
    lang: Languages
