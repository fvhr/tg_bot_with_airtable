from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inlines import create_yes_no_ikb, cancel_rating_ikb, create_answer_ikb
from loader import dp, users_table, rating_table, bot, videos_table, comments_table, user_data
from states import SendComment
from data import config


@dp.callback_query_handler(text='cancel_rating', state=SendComment)
async def cancel_comment(call: types.CallbackQuery, state: FSMContext):
    await call.answer('Отменено')
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(lambda x: x.data.startswith('point'))
async def point(call: types.CallbackQuery):
    _, rat, video_id = call.data.split('_')
    yes_no_ikb = create_yes_no_ikb(video_id)
    await bot.edit_message_text(
        text=config.AFTER_RATING_MES,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=yes_no_ikb,
        parse_mode=types.ParseMode.MARKDOWN
    )
    all_users = users_table.all()
    user_send_rating = list(filter(lambda x: x['fields']['tg_user_id'] == call.from_user.id, all_users))[0]
    rating_table.create(
        {'Оценка': int(rat), 'Заказчик который поставил': [user_send_rating['id']], 'Видео': [video_id]})


@dp.callback_query_handler(lambda x: x.data.startswith('no_comment'))
async def no_comment(call: types.CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        reply_markup=None)
    await call.answer("Хорошего дня")


@dp.callback_query_handler(lambda x: x.data.startswith('yes_comment'))
async def yes_comment(call: types.CallbackQuery):
    _, rat, vid_id = call.data.split('_')
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        reply_markup=None)
    user_data[call.from_user.id] = vid_id
    await call.message.answer('Напишите комментарий', reply_markup=cancel_rating_ikb)
    await SendComment.send.set()


@dp.message_handler(content_types=['text'], state=SendComment.send)
async def send(message: types.Message, state: FSMContext):
    await state.finish()
    video_id = user_data.get(message.from_user.id)
    getter = videos_table.get(video_id)['fields']['Исполнитель который отправил'][0]
    all_users = users_table.all()
    user_send_comment = list(filter(lambda x: x['fields']['tg_user_id'] == message.from_user.id, all_users))[0]
    comments_table.create({
        'Комментарий': message.text,
        'Видео': [video_id],
        'Отправитель': [user_send_comment['id']],
        'Получатель': [getter]
    })
    user_video = users_table.get(getter)
    video_fields = list(filter(lambda x: x['id'] == video_id, videos_table.all()))[0]['fields']
    try:
        answer_ikb = create_answer_ikb(video_id, user_send_comment['id'])
        await bot.send_message(chat_id=user_video['fields']['tg_user_id'],
                               text=f'Новый комментарий под вашим видео {video_fields["Название"]}\n'
                                    f'От {user_send_comment["fields"]["Полное имя"]}: {message.text}',
                               parse_mode=types.ParseMode.MARKDOWN,
                               reply_markup=answer_ikb)
        await message.answer('Комментарий успешно оставлен')
    except Exception:
        await message.answer('Не удалось оставить комментарий')
