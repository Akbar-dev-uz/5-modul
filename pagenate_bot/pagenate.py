import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

from pagenate_bot.get_information import DataFetcher
from quiz_handlers import router as handlers_rt
from quiz_callbacks import CategoryCallback

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
dp.include_router(handlers_rt)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Salom, {html.bold(message.from_user.full_name)}!")


@dp.message(Command('help', prefix='/%$'))
async def cmd_help(message: Message) -> None:
    await message.answer('Yordam')


@dp.message(Command('game'))
async def quiz_game(message: Message) -> None:
    df = DataFetcher()
    category = df.get_ct()
    builder = InlineKeyboardBuilder()
    for text, ct_id in category:
        builder.button(text=text, callback_data=CategoryCallback(id=ct_id))
    builder.adjust(2)
    await message.answer("Oyin boshlandi!\nKategoriyani tanglang",
                         reply_markup=builder.as_markup())


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
