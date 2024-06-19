from aiogram import types

from keyboards.inlines import creating_my_videos_ikb, create_answer_comment, create_choose_customers, cancel_answer_ikb
from loader import dp, users_table, rating_table, comments_table, videos_table, bot, user_data
from states import Answer


@dp.message_handler(text='Мои видео')
async def me_videos(message: types.Message):
    user = list(filter(lambda x: x['fields']['tg_user_id'] == message.from_user.id, users_table.all()))
    if len(user) == 0:
        pass
    else:
        if 'Исполнитель' in user[0]['fields']:
            ikb = creating_my_videos_ikb(user[0]['id'])
            await message.answer('Выберите видео по которым хотите посмотреть статистику',
                                 reply_markup=ikb)


@dp.callback_query_handler(lambda x: x.data.startswith('v_'))
async def vid(call: types.CallbackQuery):
    user_id = list(filter(lambda x: x['fields']['tg_user_id'] == call.from_user.id, users_table.all()))[0]['id']
    video_id = call.data.split('_')[1]
    all_rat = list(filter(lambda x: x['fields']['Видео'][0] == video_id, rating_table.all()))
    video_fields = videos_table.get(video_id)['fields']
    video_name = video_fields['Название']
    video_url = video_fields['Ссылка']
    if len(all_rat) == 0:
        all_ret = 1
    else:
        all_ret = len(all_rat)
    sred_rat = round(sum(list(map(lambda x: x['fields']['Оценка'], all_rat))) / all_ret, 1)
    all_comments = list(filter(lambda x: x['fields']['Видео'][0] == video_id, comments_table.all()))
    comments = sorted(all_comments, key=lambda x: x['fields']['cid'])
    message_text = f'У вашего видео [{video_name}]({video_url})\nСредний рейтинг: {sred_rat}⭐️\nКомментарии:\n\n'
    for i in range(len(comments)):
        comment_fields = comments[i]['fields']
        comment = comment_fields['Комментарий']
        try:
            sender = comment_fields['Отправитель'][0]
            if user_id == sender:
                message_text += f'От вас: {comment}\n\n'
            else:
                name = users_table.get(sender)['fields']['Полное имя']
                message_text += f'От {name}: {comment}\n\n'
        except Exception:
            message_text += 'Не удалось загрузить комментарий отправитель или получатель был удалён\n\n'
    ikb = create_answer_comment(video_id)
    await call.message.answer(message_text, parse_mode=types.ParseMode.MARKDOWN, reply_markup=ikb)


@dp.callback_query_handler(lambda x: x.data.startswith('an_comment'))
async def answ(call: types.CallbackQuery):
    video_id = call.data.split('_')[2]
    user_id = list(filter(lambda x: x['fields']['tg_user_id'] == call.from_user.id, users_table.all()))[0]['id']
    ikb = create_choose_customers(user_id, video_id)
    await bot.edit_message_reply_markup(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                        reply_markup=ikb)


@dp.callback_query_handler(lambda x: x.data.startswith('cus_'))
async def cus(call: types.CallbackQuery):
    data = call.data.split('_')
    _, video_id, getter = data
    user_data[call.from_user.id] = [video_id, getter]
    await call.message.answer('Пришлите комментарий', reply_markup=cancel_answer_ikb)
    await Answer.answer.set()
