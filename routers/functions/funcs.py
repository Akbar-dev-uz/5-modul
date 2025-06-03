from datetime import datetime as dt

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from typing import List, Union

from database.sql_alchemy import UsersMlt
from routers.states.state_for_register import StateForRegister
import re

router = Router()


def make_keyboard(options: List[Union[str, int]], row: int = 2) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for option in options:
        builder.add(KeyboardButton(text=str(option)))

    builder.adjust(row)
    return builder.as_markup(resize_keyboard=True)


def send_phone_num(text: str):
    request_phone_btn = KeyboardButton(text=text, request_contact=True)
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.add(request_phone_btn)
    phone_kb = keyboard_builder.as_markup(resize_keyboard=True)
    return phone_kb


def get_age(date_str: str) -> int:
    today = dt.today()
    date_obj = dt.strptime(date_str, "%Y-%m-%d")
    age = today.year - date_obj.year
    if (today.month, today.day) < (date_obj.month, date_obj.day):
        age -= 1
    return age


@router.message(F.text.regexp(r'^\s*\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\s*$'))
async def date_get_age(message: Message) -> None:
    age = get_age(message.text)
    await message.reply(f"Вам {age} лет!")
    print(message.from_user.full_name, message.text)


def get_date(age: str) -> str:
    today = dt.today()
    year = today.year - int(age)
    birth_date = today.replace(year=year)
    birth_date = birth_date.strftime("%Y-%m-%d")
    return birth_date


@router.message(F.text.regexp(r'^(100|[1-9]?[0-9])$'))
async def age_get_date(message: Message) -> None:
    birth_date = get_date(message.text)
    await message.answer(f"Вы родились в {birth_date}")
    print(message.from_user.full_name, message.text)


@router.message(F.text.lower() == "привет")
async def say_hello(message: Message) -> None:
    await message.reply(f"<b>Привет, {message.from_user.full_name}</b>!")
    print(message.from_user.full_name, message.text)


@router.message(F.text.lower() == "пока")
async def say_bye(message: Message) -> None:
    await message.reply(f"🫡<b>Пока, {message.from_user.full_name}</b>!")
    print(message.from_user.full_name, message.text)


@router.message(F.text.lower() == 'как дела?')
async def ans_how_are_you(message: Message) -> None:
    await message.answer(f"<b>Спасибо что спросили</b>😊\n<b>У Меня Все Отлично</b>, <b>а у вас?</b>")
    print(message.from_user.full_name, message.text)


@router.message(StateForRegister.phone)
async def num_insert(message: Message, state: FSMContext) -> None:
    phone = None

    if message.contact:
        phone = message.contact.phone_number
    elif message.text:
        phone = message.text.strip()

    if phone and not phone.startswith('+'):
        phone = '+' + phone

    pattern = r"^\+998[0-9]{9}$"

    if phone and re.fullmatch(pattern, phone):
        await state.update_data(phone_number=phone)
        await message.answer("Номер принят! Теперь введите email:")
        await state.set_state(StateForRegister.email)
    else:
        await message.answer("❌ Неверный формат номера. Пример: +998991234567")


@router.message(StateForRegister.email)
async def email_insert(message: Message, state: FSMContext) -> None:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.fullmatch(pattern, message.text):
        await message.answer("❌ Неверный формат email. Пример: example@mail.com")
        return

    await state.update_data(email=message.text)
    data = await state.get_data()
    user = UsersMlt(
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        chat_id=message.chat.id,
        user_id=message.from_user.id,
        lang=data.get("lang"),
        phone_number=data.get("phone_number"),
        email=data.get("email"),
    )
    try:
        user.save()
    except Exception as e:
        await message.answer("❌ Произошла ошибка при сохранении. Попробуйте позже.")
        print("Ошибка при сохранении:", e)
        return

    await message.answer("✅ Вы успешно зарегистрированы!")
    await state.clear()


@router.message()
async def not_exist_func(message: Message) -> None:
    await message.reply(
        f'Я не распознал такую команду, Обратитесь к <a href="https://t.me/Pulemetttka">Акбару</a> за помощью')
    print(message.from_user.full_name, message.text)
