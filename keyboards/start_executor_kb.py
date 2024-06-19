from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_executor_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отправить видео'),
         KeyboardButton(text='Мои видео')]

    ],
    one_time_keyboard=False,
    resize_keyboard=True
)