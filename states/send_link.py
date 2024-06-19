from aiogram.dispatcher.filters.state import StatesGroup, State


class SendLink(StatesGroup):
    name = State()
    link = State()