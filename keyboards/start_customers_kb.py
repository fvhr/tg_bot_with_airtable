from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_customers_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Ваши видео')]

    ],
    one_time_keyboard=False,
    resize_keyboard=True
)