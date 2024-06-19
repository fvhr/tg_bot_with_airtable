from aiogram.dispatcher.filters.state import StatesGroup, State


class SendComment(StatesGroup):
    send = State()