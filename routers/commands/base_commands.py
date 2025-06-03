from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from database.db import Database
from routers.functions.funcs import make_keyboard
from routers.keyboards.inline_keyboards import make_inline_kb
from multi_lan.db_for_mlt_lan import Database as DB_mlt_lan
from multi_lan.translate.google_tr import get_text

router = Router(name=__name__)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    db_mlt = DB_mlt_lan()
    db = Database()

    if db_mlt.check_user(message.from_user.id):
        text = get_text(message.from_user.id, message.from_user.full_name)
        await message.answer(f"{text}",
                             reply_markup=make_keyboard(["/game"], 1))
    else:
        await message.answer("Вы еще не зарегестрированы, для регистрации нажмите на /register",
                             reply_markup=make_keyboard(["/register"]))

    db.insert_users(
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
        message.chat.id,
        message.from_user.id)

    print(message.from_user.full_name, message.text)


@router.message(Command("register"))
async def command_register_handler(message: Message) -> None:
    db_mlt = DB_mlt_lan()

    if not db_mlt.check_user(message.from_user.id):
        await message.answer("Привет выберите язык!",
                             reply_markup=make_inline_kb(["🇺🇿 uz", "🇷🇺 ru", "🇺🇸 en"], ["uz", "ru", "en"], 2))
    else:
        await message.answer("Вы уже зарегестрированы😊")
    print(message.from_user.full_name, message.text)


@router.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.reply(text=f'По другим вопросам обращайтесь к <a href="https://t.me/Pulemetttka">Акбару</a>!',
                        reply_markup=make_keyboard(["/start", "/followers", "/change", "/get_currency", "/register"],
                                                   2), parse_mode=ParseMode.HTML)
    info = (
        f"chat_id = {message.chat.id}\n"
        f"user_id = {message.from_user.id}\n"
        f"text = {message.text}\n"
    )
    await message.answer(info)
    print(message.from_user.full_name, message.text)


@router.message(Command("followers"))
async def command_followers_handler(message: Message) -> None:
    db = DB_mlt_lan()
    followers = db.execute("SELECT COUNT(*) FROM users")
    await message.answer(f"Бота использовали {followers[0][0]} Пользователей🤩", reply_markup=ReplyKeyboardRemove())
    print(message.from_user.full_name, message.text)


@router.message(Command("change"))
async def command_change_lan(message: Message) -> None:
    await message.answer("Привет выберите язык!",
                         reply_markup=make_inline_kb(["🇺🇿 uz", "🇷🇺 ru", "🇺🇸 en"], ["uz", "ru", "en"], 2))
    print(message.from_user.full_name, message.text)


@router.message(Command("get_currency"))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Выберите что хотите получить",
                         reply_markup=make_inline_kb(["USD", "RUB", "EUR", "UZS"], ["USD", "RUB", "EUR", "UZS"], 2))
    print(message.from_user.full_name, message.text)
