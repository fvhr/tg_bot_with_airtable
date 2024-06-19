from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeName(StatesGroup):
    change = State()
