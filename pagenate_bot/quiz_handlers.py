from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from pagenate_bot.get_information import DataFetcher
from quiz_callbacks import *

router = Router()
df = DataFetcher()

user_quiz_data = {}


@router.callback_query(CategoryCallback.filter())
async def category_handler(call: CallbackQuery, callback_data: CallbackData):
    ct_id = callback_data.id
    sub_categories = df.get_subct(int(ct_id))
    builder = InlineKeyboardBuilder()
    for text, s_id in sub_categories:
        builder.button(text=text, callback_data=SubCategoryCallback(id=s_id, category_id=int(ct_id)))

    builder.adjust(1)
    await call.message.edit_text(text="Fanni Tangland", reply_markup=builder.as_markup())


@router.callback_query(SubCategoryCallback.filter())
async def subcategory_handler(call: CallbackQuery, callback_data: CallbackData):
    user_id = call.from_user.id
    sub_id = callback_data.id
    ct_id = callback_data.category_id
    quizzes = df.get_quiz(ct_id=ct_id, sub_id=sub_id)
    user_quiz_data[user_id] = {
        'category': callback_data.category_id,
        'subcategory': callback_data.id,
        'quizzes': quizzes,
        'current_index': 0,
        'correct_answers': 0,
        'user_answers': {}
    }
    builder = InlineKeyboardBuilder()
    for text, q_id in quizzes:
        builder.button(text=text, callback_data=QuizCallback(id=q_id, category_id=ct_id,
                                                             subcategory_id=sub_id))
        builder.adjust(2)
        await call.message.edit_text(text="Fanni Tangland", reply_markup=builder.as_markup())
