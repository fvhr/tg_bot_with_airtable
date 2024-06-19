from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_answer_ikb(video_id, user_id):
    return InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [InlineKeyboardButton(text='Ответить',
                                                          callback_data=f'answer_{video_id}_{user_id}')]
                                ])


cancel_answer_ikb = InlineKeyboardMarkup(row_width=1,
                                         inline_keyboard=[
                                             [InlineKeyboardButton(text='Отмена❌', callback_data='cancel_answer')]
                                         ])
