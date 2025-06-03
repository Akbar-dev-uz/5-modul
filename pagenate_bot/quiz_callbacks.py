from enum import Enum

from aiogram.filters.callback_data import CallbackData
from typing import Optional


class CategoryCallback(CallbackData, prefix="category"):
    id: int


# ----------------------------
class SubCategoryCallback(CallbackData, prefix="subcategory"):
    id: int
    category_id: int


# --------------------
class QuizCallback(CallbackData, prefix="quiz"):
    id: int
    subcategory_id: int
    category_id: int


class OptionCallback(CallbackData, prefix="option"):
    id: int
    category_id: int
    subcategory_id: int
    quiz_id: int


class Level(Enum):
    CATEGORY = 'category'
    SUBCATEGORY = 'subcategory'
    QUIZ_START = 'quiz_start'
    QUIZ = 'quiz'


class BackCallback(CallbackData, prefix='back'):
    level: str
    category: Optional[int] = None
    subcategory: Optional[int] = None
    quiz: Optional[int] = None
