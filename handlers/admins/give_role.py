from aiogram import types

from keyboards import start_executor_kb
from keyboards.inlines import roles_ikb, do_role_ikb
from loader import dp, users_table, bot
from data import config


@dp.message_handler(text='Роли')
async def rol(message: types.Message):
    all_users = users_table.all()
    messages = config.START_CUSTOMERS_MES
    user = list(filter(lambda x: x['fields']['tg_user_id'] == message.from_user.id, all_users))
    if len(user) == 0:
        await message.answer(messages)
    else:
        if 'Администратор' in user[0]['fields']:
            await message.answer('Выберите действие', reply_markup=do_role_ikb)


@dp.callback_query_handler(text='give_role')
async def give_role(call: types.CallbackQuery):
    ikb = roles_ikb()
    await call.message.answer('Выберите кому хотите выдать роль', reply_markup=ikb)


@dp.callback_query_handler(lambda x: x.data.startswith('give_'))
async def give(call: types.CallbackQuery):
    all_users = users_table.all()
    _, tg_id = call.data.split('_')
    user = list(filter(lambda x: x['fields']['tg_user_id'] == int(tg_id), all_users))[0]
    users_table.update(user['id'], {
        'Заказчик': False,
        'Исполнитель': True
    })
    try:
        await bot.send_message(int(tg_id), 'Вам выдпли права исполнителя вам доступны новые возможности',
                               reply_markup=start_executor_kb)
    except:
        pass
    await call.message.answer(f'Пользователю {user["fields"]["Полное имя"]} успешно выданы права исполнителя')
