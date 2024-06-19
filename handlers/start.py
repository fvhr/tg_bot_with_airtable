from aiogram import types

from keyboards import start_admin_kb, start_executor_kb, start_customers_kb
from loader import dp, users_table
from data import config


@dp.message_handler(text='/start')
async def start(message: types.Message):
    all_users = users_table.all()
    user = list(filter(lambda x: x['fields']['tg_user_id'] == message.from_user.id, all_users))
    if len(user) == 0:
        users_table.create({'tg_user_id': message.from_user.id, 'Полное имя': message.from_user.full_name,
                            'Заказчик': True})
        await message.answer(
            config.START_CUSTOMERS_MES.replace('[имя]', message.from_user.full_name),
            reply_markup=start_customers_kb)
    else:
        user_fields = user[0]['fields']
        full_name = user_fields['Полное имя']
        if 'Администратор' in user_fields:
            await message.answer(config.START_ADMIN_MES.replace('[имя]', full_name),
                                 reply_markup=start_admin_kb)
        elif 'Исполнитель' in user_fields:
            await message.answer(config.START_EXECUTOR_MES.replace('[имя]', full_name),
                                 reply_markup=start_executor_kb)
