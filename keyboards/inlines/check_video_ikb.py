from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import rating_table, videos_table


def creating_check_video_ikb(customer_id):
    try:
        all_rating = list(filter(lambda x: x['fields']['Заказчик который поставил'][0] == customer_id, rating_table.all()))
    except Exception as e:
        print(e)

    all_rating = []

    ikb = InlineKeyboardMarkup()
    for rat in all_rating:
        video_id = rat['fields']['Видео'][0]
        video_name = videos_table.get(video_id)['fields']['Название']
        ikb.add(InlineKeyboardButton(text=video_name, callback_data=f'video_{video_id}'))
    return ikb


def create_write_comment(video_id, getter):
    return InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [InlineKeyboardButton(text='Написать комментарий',
                                                          callback_data=f'write_comment_{video_id}_{getter}')]
                                ])
