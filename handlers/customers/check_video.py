from aiogram import types

from keyboards.inlines import creating_check_video_ikb, create_write_comment, cancel_answer_ikb
from loader import dp, users_table, rating_table, videos_table, comments_table, user_data
from states import Answer
from data import config


@dp.message_handler(text='Ваши видео')
async def you_videos(message: types.Message):
    user = list(filter(lambda x: x['fields']['tg_user_id'] == message.from_user.id, users_table.all()))
    if len(user) == 0:
        await message.answer(config.START_CUSTOMERS_MES)
    else:
        if 'Заказчик' in user[0]['fields']:
            ikb = creating_check_video_ikb(user[0]['id'])
            await message.answer('Здесь видео на которые вы когда любо оставляли комментарий или оценку',
                                 reply_markup=ikb)


@dp.callback_query_handler(lambda x: x.data.startswith('video_'))
async def vid(call: types.CallbackQuery):
    user_id = list(filter(lambda x: x['fields']['tg_user_id'] == call.from_user.id, users_table.all()))[0]['id']
    video_id = call.data.split('_')[1]
    rat = list(
        filter(lambda x: x['fields']['Видео'][0] == video_id and x['fields']['Заказчик который поставил'][0] == user_id,
               rating_table.all()))[0]['fields']['Оценка']
    video_fields = videos_table.get(video_id)['fields']
    creator_id = video_fields['Исполнитель который отправил'][0]
    video_name = video_fields['Название']
    video_url = video_fields['Ссылка']
    comments = list(
        filter(lambda x: x['fields']['Видео'][0] == video_id and (x['fields']['Отправитель'][0] == user_id or
                         x['fields']['Получатель'][0] == user_id),
               comments_table.all()))
    comments = sorted(comments, key=lambda x: x['fields']['cid'])
    message_text = f'Вы поставили видео [{video_name}]({video_url}) {rat}⭐️\nКомментарии:\n'
    for i in range(len(comments)):
        comment_fields = comments[i]['fields']
        comment = comment_fields['Комментарий']
        sender = comment_fields['Отправитель'][0]
        if user_id == sender:
            message_text += f'От вас: {comment}\n\n'
        else:
            name = users_table.get(creator_id)['fields']['Полное имя']
            message_text += f'От {name}: {comment}\n\n'
    ikb = create_write_comment(video_id, creator_id)
    await call.message.answer(text=message_text, parse_mode=types.ParseMode.MARKDOWN, reply_markup=ikb)


@dp.callback_query_handler(lambda x: x.data.startswith('write_comment'))
async def write_comment(call: types.CallbackQuery):
    _, _, vid_id, user_id = call.data.split('_')
    user_data[call.from_user.id] = [vid_id, user_id]
    await call.message.answer('Пришлите комментарий', reply_markup=cancel_answer_ikb)
    await Answer.answer.set()