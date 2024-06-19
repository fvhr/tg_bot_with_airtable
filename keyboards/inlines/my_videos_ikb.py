from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import videos_table, comments_table, users_table


def creating_my_videos_ikb(customer_id):
    all_videos = list(
        filter(lambda x: x['fields']['Исполнитель который отправил'][0] == customer_id, videos_table.all()))
    ikb = InlineKeyboardMarkup()
    for video in all_videos:
        video_id = video['id']
        video_name = video['fields']['Название']
        ikb.add(InlineKeyboardButton(text=video_name, callback_data=f'v_{video_id}'))
    return ikb


def create_choose_customers(user_id, video_id):
    all_comments = list(filter(lambda x: x['fields']['Видео'][0] == video_id and 'Отправитель' in x['fields'] and
                                         x['fields']['Отправитель'][0] != user_id, comments_table.all()))
    all_customers_id = set(map(lambda x: x['fields']['Отправитель'][0], all_comments))
    ikb = InlineKeyboardMarkup()
    for customer_id in all_customers_id:
        customer_name = users_table.get(customer_id)['fields']['Полное имя']
        ikb.add(InlineKeyboardButton(text=customer_name, callback_data=f'cus_{video_id}_{customer_id}'))
    return ikb


def create_answer_comment(video_id):
    return InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                    [InlineKeyboardButton(text='Ответить на комментарий',
                                                          callback_data=f'an_comment_{video_id}')]
                                ])
