from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import F, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

from database.db import db
from api.get_valute import get_currency
from routers.states.state_for_register import StateForRegister
from routers.functions.funcs import send_phone_num
from .callbacks import Language, Languages
from aiogram.utils.i18n import gettext as _

router = Router()


def make_inline_kb(texts: list[str], callback_data: list, row):
    builder = InlineKeyboardBuilder()
    builder.add(
        *[InlineKeyboardButton(text=text, callback_data=callbackdt) for text, callbackdt in zip(texts, callback_data)])
    builder.adjust(row)
    return builder.as_markup()


def kb_for_langs():
    kb = make_inline_kb(["🇺🇿 uz", "🇷🇺 ru", "🇺🇸 en"],
                        [Language(lang=Languages.UZ.value).pack(), Language(lang=Languages.RU.value).pack(),
                         Language(lang=Languages.EN.value).pack()], 2)
    return kb


@router.callback_query(Language.filter())
async def catch_uz(call: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    user_id = call.from_user.id
    username = call.from_user.username or "Unknown"
    lang = str(callback_data.lang.value)
    print(f"Processing language change to '{lang}' for user_id={user_id}, username={username}")

    await call.message.edit_text(_("✅ Language selected"))

    if db.check_user_mlt(user_id):
        result = db.execute(
            "UPDATE users_mlt_lan SET lang = :lang WHERE user_id = :user_id",
            {'lang': lang, 'user_id': user_id}, fetch=False
        )
        print(f"Update result for user_id={user_id}: {result}")
        if result is None:
            await call.message.answer(_("❌ Ошибка при обновлении языка."))
            return
        if result == 0:
            await call.message.answer(_("❌ Пользователь не найден в базе данных."))
            return
        await call.message.answer(_("✅ Язык успешно обновлен!"))
        return
    await state.update_data(lang=lang)
    text = _("📱 Telefon nomeringizni kiriting:")
    await call.message.answer(text, reply_markup=send_phone_num(text))
    await state.set_state(StateForRegister.phone)


@router.callback_query(F.data.in_(["USD", "RUB", "EUR", "UZS"]))
async def catch_currency(call: CallbackQuery):
    currency = call.data
    data = get_currency(currency)
    data_str = "\n".join(f"{k}: {v}" for k, v in data.items())
    await call.message.edit_text(data_str, reply_markup=make_inline_kb(
        [f"{currency}_TO_USD", f"{currency}_TO_RUB", f"{currency}_TO_EUR", f"{currency}_TO_UZS"],
        [f"{currency}_TO_USD", f"{currency}_TO_RUB", f"{currency}_TO_EUR", f"{currency}_TO_UZS"], 2))
    print(call.message.from_user.username, ":", currency)


@router.callback_query(F.data.in_([
    'USD_TO_USD', 'USD_TO_RUB', 'USD_TO_EUR', 'USD_TO_UZS',
    'RUB_TO_USD', 'RUB_TO_RUB', 'RUB_TO_EUR', 'RUB_TO_UZS',
    'EUR_TO_USD', 'EUR_TO_RUB', 'EUR_TO_EUR', 'EUR_TO_UZS',
    'UZS_TO_USD', 'UZS_TO_RUB', 'UZS_TO_EUR', 'UZS_TO_UZS'
]))
async def catch_currency_to(call: CallbackQuery):
    s = call.data
    currency, to_currency = s.split("_TO_")
    data = get_currency(currency, to_currency)
    await call.message.edit_text(f"{s}\n{data}")
    print(call.message.from_user.username, ":", s)
