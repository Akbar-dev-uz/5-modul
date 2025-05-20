import asyncio
from dataclasses import dataclass

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from database.db import Database
from routers.functions.funcs import make_keyboard


router = Router()
db = Database()


@dataclass
class Question:
    text: str
    options: list[str]
    correct_answer: str


class GameState(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()


matematika = [
    Question(text='2 * 4 = ?', options=['8', '9', '10', '11'], correct_answer='8'),
    Question(text='2 - 4 = ?', options=['-2', '3', '0', '1'], correct_answer='-2'),
    Question(text='2x * 4 = 0', options=['0', '9', '10', '11'], correct_answer='0'),
]


@router.message(Command("game"))
async def game_start(message: Message, state: FSMContext):
    m = matematika[0]
    await message.answer(f"{m.text}", reply_markup=make_keyboard(m.options, 2))
    await state.set_state(GameState.q1)
    print(message.from_user.full_name, message.text)


@router.message(GameState.q1)
async def get_q1(message: Message, state: FSMContext):
    m = matematika[0]
    answ = True if message.text == m.correct_answer else False
    m = matematika[1]
    await state.update_data(q1=f"{message.text} - {answ}")
    await message.answer(f"{m.text}", reply_markup=make_keyboard(m.options, 2))
    await state.set_state(GameState.q2)
    print(message.from_user.full_name, message.text)


@router.message(GameState.q2)
async def get_q3(message: Message, state: FSMContext):
    m = matematika[1]
    answ = True if message.text == m.correct_answer else False
    m = matematika[2]
    await state.update_data(q2=f"{message.text} - {answ}")
    await message.answer(f"{m.text}", reply_markup=make_keyboard(m.options, 2))
    await state.set_state(GameState.q3)
    print(message.from_user.full_name, message.text)


@router.message(GameState.q3)
async def finish_quiz(message: Message, state: FSMContext):
    m = matematika[2]
    answ = True if message.text == m.correct_answer else False
    await state.update_data(q3=f"{message.text} - {answ}")

    data = await state.get_data()
    results = f'<b>Результаты:</b>\nq1={data.get("q1")}\nq2={data.get("q2")}\nq3={data.get("q3")}'

    await message.answer(results, reply_markup=ReplyKeyboardRemove())
    await state.clear()

    def get_in_base():
        db.db_for_game()
        db.insert_games(message.from_user.username, message.chat.id, message.from_user.id, "Matematika",
                        results)

    await asyncio.to_thread(get_in_base)

    print(message.from_user.full_name, message.text)
