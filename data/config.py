import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))
AIR_TABLE_TOKEN = str(os.getenv('AIR_TABLE_TOKEN'))
AIR_TABLE_APP_NAME = str(os.getenv('AIR_TABLE_APP_NAME'))
AIR_TABLE_USERS = str(os.getenv('AIR_TABLE_USERS'))
AIR_TABLE_TEMPLATE_MESSAGES = str(os.getenv('AIR_TABLE_TEMPLATE_MESSAGES'))
AIR_TABLE_VIDEOS = str(os.getenv('AIR_TABLE_VIDEOS'))
AIR_TABLE_RATING = str(os.getenv('AIR_TABLE_RATING'))
AIR_TABLE_COMMENTS = str(os.getenv('AIR_TABLE_COMMENTS'))


START_ADMIN_MES = ""
START_CUSTOMERS_MES = ""
START_EXECUTOR_MES = ""
LINK_MES = ""
AFTER_RATING_MES = ""
ANSWER_MES = ""