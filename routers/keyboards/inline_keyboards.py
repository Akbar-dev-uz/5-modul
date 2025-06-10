from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import F, Router

from database.db import db
from api.get_valute import get_currency
from routers.states.state_for_register import StateForRegister
from routers.functions.funcs import send_phone_num

router = Router()


def make_inline_kb(texts: list[str], callback_data: list[str], row):
    if len(texts) != len(callback_data):
        raise Exception("Incorrect given options")
    buttons = [InlineKeyboardButton(text=text, callback_data=data)
               for text, data in zip(texts, callback_data)]
    keyboard_layout = [buttons[i:i + row] for i in range(0, len(buttons), row)]
    return InlineKeyboardMarkup(inline_keyboard=keyboard_layout)


@router.callback_query(F.data == 'uz')
async def catch_uz(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("🇺🇿Siz o`zbek tilini tanglandingiz!")
    if db.check_user_mlt(call.from_user.id):
        db.execute("UPDATE users_mlt_lan SET lang = %s WHERE user_id = %s", [('uz', call.from_user.id,)])
        return
    await state.update_data(lang='uz')
    text = "📱 Telefon nomeringizni kiriting:"
    await call.message.answer(text, reply_markup=send_phone_num(text))
    await state.set_state(StateForRegister.phone)


@router.callback_query(F.data == 'ru')
async def catch_ru(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("🇷🇺Вы выбрали русский язык!")
    if db.check_user_mlt(call.from_user.id):
        db.execute("UPDATE users_mlt_lan SET lang = %s WHERE user_id = %s", ('ru', call.from_user.id,))
        return
    await state.update_data(lang='ru')
    text = "📱 Введите телефон номер:"
    await call.message.answer(text, reply_markup=send_phone_num(text))
    await state.set_state(StateForRegister.phone)


@router.callback_query(F.data == 'en')
async def catch_en(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("🇺🇸You chosen English language!")
    if db.check_user_mlt(call.from_user.id):
        db.execute("UPDATE users_mlt_lan SET lang = %s WHERE user_id = %s", ('en', call.from_user.id,))
        return
    await state.update_data(lang='en')
    text = "📱 Get your phone number:"
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
