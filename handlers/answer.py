from aiogram import types
from aiogram.dispatcher import FSMContext

from data import config
from keyboards.inlines import cancel_answer_ikb, create_answer_ikb
from loader import dp, bot, users_table, comments_table, videos_table, user_data
from states import Answer


@dp.callback_query_handler(text='cancel_answer', state=Answer)
async def cancel_answer(call: types.CallbackQuery, state: FSMContext):
    await call.answer('Отменено')
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(lambda x: x.data.startswith('answer_'))
async def answer(call: types.CallbackQuery):
    _, vid_id, user_id = call.data.split('_')
    user_data[call.from_user.id] = [vid_id, user_id]
    await call.message.answer('Напишите ответ на комментарий', reply_markup=cancel_answer_ikb)
    await Answer.answer.set()


@dp.message_handler(content_types=['text'], state=Answer.answer)
async def answ(message: types.Message, state: FSMContext):
    await state.finish()
    vid_id, user_id = user_data[message.from_user.id]
    all_users = users_table.all()
    user_send_comment = list(filter(lambda x: x['fields']['tg_user_id'] == message.from_user.id, all_users))[0]
    comments_table.create({
        'Комментарий': message.text,
        'Видео': [vid_id],
        'Отправитель': [user_send_comment['id']],
        'Получатель': [user_id]
    })
    # video_fields = list(filter(lambda x: x['id'] == vid_id, videos_table.all()))[0]['fields']
    tg_user_id = users_table.get(user_id)['fields']['tg_user_id']
    try:
        answer_ikb = create_answer_ikb(vid_id, user_send_comment['id'])
        text = config.ANSWER_MES.replace('[имя]', user_send_comment["fields"]["Полное имя"]).replace('[ответ]',
                                                                                                     message.text)
        await bot.send_message(chat_id=tg_user_id,
                               text=text,
                               parse_mode=types.ParseMode.MARKDOWN,
                               reply_markup=answer_ikb)
        await message.answer('Ответ успешно оставлен')
    except Exception:
        await message.answer('Не удалось оставить ответ')
