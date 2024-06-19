from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inlines import cancel_link_ikb, creating_rating_ikb
from loader import dp, users_table, bot, videos_table
from states import SendLink
from data import config


@dp.callback_query_handler(text='cancel_send_link', state=SendLink)
async def cancel_link(call: types.CallbackQuery, state: FSMContext):
    await call.answer('Отменено')
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(text='Отправить видео')
async def send_link(message: types.Message):
    all_users = users_table.all()
    user = list(filter(lambda x: x['fields']['tg_user_id'] == message.from_user.id, all_users))
    if len(user) == 0:
        pass
    else:
        if 'Исполнитель' in user[0]['fields']:
            await message.answer('Пришлите название видео', reply_markup=cancel_link_ikb)
            await SendLink.name.set()


@dp.message_handler(content_types=['text'], state=SendLink.name)
async def send_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Пришлите ссылку на видео', reply_markup=cancel_link_ikb)
    await SendLink.link.set()


@dp.message_handler(content_types=['text'], state=SendLink.link)
async def s_link(message: types.Message, state: FSMContext):
    link = message.text
    if not link.startswith('https://'):
        await message.answer('Это не ссылка попробуйте снова', reply_markup=cancel_link_ikb)
    else:
        link_message = config.LINK_MES.replace('(ссылка)', link)
        all_users = users_table.all()
        customers = list(filter(lambda x: 'Заказчик' in x['fields'], all_users))
        user_send_link = list(filter(lambda x: x['fields']['tg_user_id'] == message.from_user.id, all_users))[0]
        data = await state.get_data()
        name = data['name']
        video = videos_table.create(
            {'Название': name, 'Ссылка': link, 'Исполнитель который отправил': [user_send_link['id']]})
        for customer in customers:
            tg_customer_id = customer['fields']['tg_user_id']
            full_name = customer['fields']['Полное имя']
            send_message = link_message.replace('[имя]', full_name).replace('[название]', name)
            try:
                ikb = creating_rating_ikb(video['id'])
                await bot.send_message(chat_id=tg_customer_id, text=send_message, reply_markup=ikb,
                                       parse_mode=types.ParseMode.MARKDOWN)
            except Exception:
                pass
        await message.answer('Видео успешно отправлено')
        await state.finish()
