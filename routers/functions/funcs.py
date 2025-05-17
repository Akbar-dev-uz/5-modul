from datetime import datetime as dt

from aiogram import Router, F
from aiogram.types import Message

router = Router()


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


@router.message()
async def not_exist_func(message: Message) -> None:
    await message.reply(
        f'Я не распознал такую команду, Обратитесь к <a href="https://t.me/Pulemetttka">Акбару</a> за помощью')
    print(message.from_user.full_name, message.text)
