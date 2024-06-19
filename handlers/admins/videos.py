from aiogram import types

from keyboards.inlines import create_video_ikb, create_answer_comment
from loader import dp, videos_table, users_table, rating_table, comments_table


@dp.message_handler(text='Видео')
async def videos(message: types.Message):
    ikb = create_video_ikb()
    await message.answer('Выберите видео', reply_markup=ikb)


@dp.callback_query_handler(lambda x: x.data.startswith('all_v_'))
async def vi(call: types.CallbackQuery):
    _, _, video_id = call.data.split('_')
    user_id = list(filter(lambda x: x['fields']['tg_user_id'] == call.from_user.id, users_table.all()))[0]['id']
    video = videos_table.get(video_id)
    creator = users_table.get(video['fields']['Исполнитель который отправил'][0])
    all_rat = list(filter(lambda x: x['fields']['Видео'][0] == video_id, rating_table.all()))
    if len(all_rat) == 0:
        all_ret = 1
    else:
        all_ret = len(all_rat)
    sred_rat = round(sum(list(map(lambda x: x['fields']['Оценка'], all_rat))) / all_ret, 1)
    all_comments = list(filter(lambda x: x['fields']['Видео'][0] == video_id, comments_table.all()))
    comments = sorted(all_comments, key=lambda x: x['fields']['cid'])
    message_text = (
        f'Видео [{video["fields"]["Название"]}]({video["fields"]["Ссылка"]})\nСоздатель: '
        f'{creator["fields"]["Полное имя"]}\nСредний рейтинг: '
        f'{sred_rat}⭐️\nКомментарии:\n\n')
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
