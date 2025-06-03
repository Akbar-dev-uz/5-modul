import uuid
from os import getenv

from aiogram import html, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Salom, {html.bold(message.from_user.full_name)}!")


@start_router.inline_query()
async def inline_query_handler(query: InlineQuery) -> None:
    query_text = query.query.lower().strip()

    results = InlineQueryResultArticle(
        id=str(uuid.uuid4()),
        title="Salom",
        text=f"",
    )

# @router.inline_query()
# async def inline_query_handler(inline_query: InlineQuery):
#     query_text = inline_query.query.strip()
#
#     if not query_text:
#         return
#
#     results = [
#         InlineQueryResultArticle(
#             id=str(uuid.uuid4()),  # уникальный ID
#             title=f"Вариант {i + 1}: {query_text}",
#             input_message_content=InputTextMessageContent(
#                 message_text=f"Результат {i + 1}: <b>{query_text}</b>"
#             ),
#             description=f"Отправить результат {i + 1}",
#         )
#         for i in range(5)
#     ]
#
#     await inline_query.answer(results, cache_time=1)
