from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inlines import create_remove, create_change, create_change_fields, cancel_change_ikb
from keyboards import start_customers_kb
from loader import dp, bot, users_table, user_data
from states import ChangeName


@dp.callback_query_handler(text='cancel_change', state=ChangeName)
async def canc(call: types.CallbackQuery, state: FSMContext):
    await call.answer('Отменено')
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(text='remove_role')
async def remove_role(call: types.CallbackQuery):
    ikb = create_remove()
    await call.message.answer('Выберите у кого хотите забрать роль', reply_markup=ikb)


@dp.callback_query_handler(lambda x: x.data.startswith('remove_'))
async def rem(call: types.CallbackQuery):
    _, tg_id, user_id = call.data.split('_')
    try:
        users_table.update(user_id, {'Исполнитель': False, 'Заказчик': True})
        await bot.send_message(chat_id=int(tg_id), text='У вас забрали роль исполнителя',
                               reply_markup=start_customers_kb)
    except:
        pass
    await call.message.answer('У пользователя забрана роль')


@dp.callback_query_handler(text='change')
async def change(call: types.CallbackQuery):
    ikb = create_change()
    await call.message.answer('Выберите кого хотите изменить', reply_markup=ikb)


@dp.callback_query_handler(lambda x: x.data.startswith('change_'))
async def cha(call: types.CallbackQuery):
    _, user_id = call.data.split('_')
    user = users_table.get(user_id)
    if 'Администратор' in user['fields']:
        role = 'Администратор'
    elif 'Заказчик' in user['fields']:
        role = 'Заказчик'
    else:
        role = 'Исполнитель'
    ikb = create_change_fields(user_id)
    await call.message.answer(f'UID: {user_id}\nИмя: {user["fields"]["Полное имя"]}\nРоль: {role}', reply_markup=ikb)


@dp.callback_query_handler(lambda x: x.data.startswith('ch_name'))
async def ch_name(call: types.CallbackQuery):
    _, _, user_id = call.data.split('_')
    user_data[call.from_user.id] = user_id
    await call.message.answer('Введите новое имя пользователя', reply_markup=cancel_change_ikb)
    await ChangeName.change.set()


@dp.message_handler(content_types=['text'], state=ChangeName.change)
async def ch(message: types.Message, state: FSMContext):
    user_id = user_data[message.from_user.id]
    await state.finish()
    users_table.update(user_id, {'Полное имя': message.text})
    await message.answer('Имя успешно изменено')
