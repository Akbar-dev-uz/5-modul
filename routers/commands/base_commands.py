from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove

from database.db import db, User
from routers.functions.funcs import make_keyboard
from routers.keyboards.inline_keyboards import make_inline_kb
from aiogram.utils.i18n import gettext as _

router_base = Router(name=__name__)


@router_base.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if db.check_user_mlt(message.from_user.id):
        await message.answer(text=_("start").format(full_name=message.from_user.full_name),
                             reply_markup=make_keyboard(["/game"], 1))
    else:
        await message.answer(_("Вы еще не зарегистрированы, для регистрации нажмите на /register"),
                             reply_markup=make_keyboard(["/register"]))
    user = User(
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        chat_id=message.chat.id,
        user_id=message.from_user.id
    )
    db.save(user)

    print(message.from_user.full_name, message.text)


@router_base.message(Command("register"))
async def command_register_handler(message: Message) -> None:
    if not db.check_user_mlt(message.from_user.id):
        await message.answer(_("Привет выберите язык!"),
                             reply_markup=make_inline_kb(["🇺🇿 uz", "🇷🇺 ru", "🇺🇸 en"], ["uz", "ru", "en"], 2))
    else:
        await message.answer(_("Вы уже зарегистрированы😊"))
    print(message.from_user.full_name, message.text)


@router_base.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.reply(text=f'По другим вопросам обращайтесь к <a href="https://t.me/Pulemetttka">Акбару</a>!',
                        reply_markup=make_keyboard(
                            ["/start", "/followers", "/change", "/get_currency", "/register"],
                            2), parse_mode=ParseMode.HTML)
    info = (
        f"chat_id = {message.chat.id}\n"
        f"user_id = {message.from_user.id}\n"
        f"text = {message.text}\n"
    )
    await message.answer(info)
    print(message.from_user.full_name, message.text)


@router_base.message(Command("followers"))
async def command_followers_handler(message: Message) -> None:
    followers = db.execute("SELECT COUNT(*) FROM users")
    await message.answer(f"Бота использовали {followers[0][0]} Пользователей🤩", reply_markup=ReplyKeyboardRemove())
    print(message.from_user.full_name, message.text)


@router_base.message(Command("change"))
async def command_change_lan(message: Message) -> None:
    await message.answer("Привет выберите язык!",
                         reply_markup=make_inline_kb(["🇺🇿 uz", "🇷🇺 ru", "🇺🇸 en"], ["uz", "ru", "en"], 2))
    print(message.from_user.full_name, message.text)


@router_base.message(Command("get_currency"))
async def get_currency(message: Message) -> None:
    await message.answer(f"Выберите что хотите получить",
                         reply_markup=make_inline_kb(["USD", "RUB", "EUR", "UZS"], ["USD", "RUB", "EUR", "UZS"], 2))
    print(message.from_user.full_name, message.text)
