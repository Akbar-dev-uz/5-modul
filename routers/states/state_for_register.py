from aiogram.fsm.state import State, StatesGroup


class StateForRegister(StatesGroup):
    phone = State()
    email = State()
