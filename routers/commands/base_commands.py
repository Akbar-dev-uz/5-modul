from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove

from database.db import db, User
from routers.functions.funcs import make_keyboard
from routers.keyboards.inline_keyboards import make_inline_kb, kb_for_langs
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
    if not db.check_user(message.from_user.id):
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
                             reply_markup=kb_for_langs())
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
    result = db.execute("SELECT COUNT(*) AS count FROM users")
    count = result.scalar()
    await message.answer(f"Бота использовали {count} Пользователей🤩", reply_markup=ReplyKeyboardRemove())
    print(message.from_user.full_name, message.text)


@router_base.message(Command("change"))
async def command_change_lan(message: Message) -> None:
    await message.answer("Привет выберите язык!",
                         reply_markup=kb_for_langs())
    print(message.from_user.full_name, message.text)


@router_base.message(Command("get_currency"))
async def get_currency(message: Message) -> None:
    await message.answer(f"Выберите что хотите получить",
                         reply_markup=make_inline_kb(["USD", "RUB", "EUR", "UZS"], ["USD", "RUB", "EUR", "UZS"], 2))
    print(message.from_user.full_name, message.text)


@router_base.message(Command("check"))
async def get_currency(message: Message) -> None:
    await message.answer(_("Salom {full_name}!").format(full_name=message.from_user.full_name))
    print(message.from_user.full_name, message.text)
