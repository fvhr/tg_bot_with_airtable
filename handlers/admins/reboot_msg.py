from loader import api
from loader import dp
from data import config
from aiogram import types


@dp.message_handler(text='Обновить текст')
async def reboot_msg(message: types.Message):
    all_message_fields = api.table(config.AIR_TABLE_APP_NAME, config.AIR_TABLE_TEMPLATE_MESSAGES).all()[0]['fields']

    config.START_ADMIN_MES = all_message_fields['start_admin_message']
    config.START_CUSTOMERS_MES = all_message_fields['start_customers_message']
    config.START_EXECUTOR_MES = all_message_fields['start_executor_message']
    config.LINK_MES = all_message_fields['link_message']
    config.AFTER_RATING_MES = all_message_fields['after_rating_message']
    config.ANSWER_MES = all_message_fields['answer_mes']
    print(111)

    if message != None:
        await message.answer("Текст обновлён")
