
from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import wikipedia

wiki_router = Router()


@wiki_router.inline_query()
async def inline_query_handler(inline_query: InlineQuery):
    word = inline_query.query.lower().strip()
    # print(f"Query Word: {word}")
    # wikipedia.set_lang('uz')
    #
    # results = wikipedia.search(word)
    # for index, title in enumerate(results):
    #     print(f"idx: {index}. {title}")
    #
    # idx = int(input('index: '))
    # obj = wikipedia.page(results[idx])
    # print(obj.title)
    # print(obj.url)
    # print(obj.content)
    results = []
    if not word:
        results.append(InlineQueryResultArticle(
            id=str(1),
            title="🤔 Hech narsa yo'q!",
            description=f"\"{word}\" haqida ma'lumot topilmadi!",
            thumbnail_url='https://pngimg.com/d/wikipedia_PNG38.png',
            input_message_content=InputTextMessageContent(
                message_text=f"☹️ \"{word}\" haqida ma'lumot topilmadi!"
            )

        ))
        return inline_query.answer(results, cache_time=1)
