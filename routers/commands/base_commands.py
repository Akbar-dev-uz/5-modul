from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from database.db import Database

router = Router(name=__name__)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    db = Database()
    await message.answer(f"<b>Привет, {message.from_user.full_name}</b>!")
    db.insert_users(message.from_user.username,
                    message.from_user.first_name,
                    message.from_user.last_name,
                    message.chat.id,
                    message.from_user.id)


@router.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.reply(f'Обратитесь за помощью к <a href="https://t.me/Pulemetttka">Акбару</a> за помощью')
    print(message.from_user.full_name, message.text)
    info = (
        f"chat_id = {message.chat.id}\n"
        f"user_id = {message.from_user.id}\n"
        f"text = {message.text}\n"
    )
    await message.answer(info)


@router.message(Command("followers"))
async def command_followers_handler(message: Message) -> None:
    db = Database()
    followers = db.execute("SELECT COUNT(*) FROM users")
    followers = followers.fetchall()
    await message.answer(f"Бота использовали {followers[0][0]} Пользователей🤩")
