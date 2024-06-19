from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

start_admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Роли'), KeyboardButton(text='Видео')],
        [KeyboardButton(text='Редактировать текст', web_app=WebAppInfo(
            url='https://airtable.com/appMutAAvoLOCBbRL/tblO3dtbFf6rvxgju/viwRa4AKZDHsHqlDA?blocks=hide')), KeyboardButton(text='Обновить текст')]

    ],
    one_time_keyboard=False,
    resize_keyboard=True
)
