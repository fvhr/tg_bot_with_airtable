from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def creating_rating_ikb(video_id):
    return InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [InlineKeyboardButton(text='1⭐️', callback_data=f'point_1_{video_id}'),
                                     InlineKeyboardButton(text='2⭐️', callback_data=f'point_2_{video_id}'),
                                     InlineKeyboardButton(text='3⭐️', callback_data=f'point_3_{video_id}'),
                                     InlineKeyboardButton(text='4⭐️', callback_data=f'point_4_{video_id}'),
                                     InlineKeyboardButton(text='5⭐️', callback_data=f'point_5_{video_id}')]
                                ])


def create_yes_no_ikb(video_id):
    return InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [InlineKeyboardButton(text='Да', callback_data=f'yes_comment_{video_id}'),
                                     InlineKeyboardButton(text='Нет', callback_data=f'no_comment_{video_id}')]
                                ])


cancel_rating_ikb = InlineKeyboardMarkup(row_width=1,
                                         inline_keyboard=[
                                             [InlineKeyboardButton(text='Отмена❌', callback_data='cancel_rating')]
                                         ])
