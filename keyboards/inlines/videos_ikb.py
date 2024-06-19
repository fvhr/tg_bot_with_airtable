from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import videos_table


def create_video_ikb():
    all_videos = videos_table.all()
    videos_ikb = InlineKeyboardMarkup()
    for video in all_videos:
        videos_ikb.add(InlineKeyboardButton(text=video['fields']['Название'], callback_data=f'all_v_{video["id"]}'))
    return videos_ikb
