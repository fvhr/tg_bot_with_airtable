from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pyairtable import Api
from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
api = Api(config.AIR_TABLE_TOKEN)
users_table = api.table(config.AIR_TABLE_APP_NAME, config.AIR_TABLE_USERS)
videos_table = api.table(config.AIR_TABLE_APP_NAME, config.AIR_TABLE_VIDEOS)
rating_table = api.table(config.AIR_TABLE_APP_NAME, config.AIR_TABLE_RATING)
comments_table = api.table(config.AIR_TABLE_APP_NAME, config.AIR_TABLE_COMMENTS)
user_data = {}
