import asyncio
import logging
import random
from dataclasses import dataclass, field
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


@dataclass
class Question:
    text: str
    options: list[str]
    correct_answer: str


@dataclass
class Database:
    questions: list[Question]


matematika = [
    Question(text='2 * 4 = ?', options=['8', '9', '10', '11'], correct_answer='8'),
    Question(text='2 - 4 = ?', options=['-2', '3', '0', '1'], correct_answer='-2'),
    Question(text='2x * 4 = 0', options=['0', '9', '10', '11'], correct_answer='0'),
]

# biologiya = [
#     Question(text='2 * 4 = ?', options=['8', '9', '10', '11'], correct_answer='8'),
#     Question(text='2 - 4 = ?', options=['-2', '3', '0', '1'], correct_answer='-2'),
#     Question(text='2x * 4 = 0', options=['0', '9', '10', '11'], correct_answer='0'),
# ]

db = Database(questions=matematika)
# db.extend(matematika)
# db.extend(biologiya)
print(db)

dp['quizzes'] = db


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Salom, {html.bold(message.from_user.full_name)}!")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
