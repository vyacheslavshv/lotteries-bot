import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_NAME = os.getenv('BOT_NAME')
BOT_CHANNEL = os.getenv('BOT_CHANNEL')

MANIFEST_URL = os.getenv('MANIFEST_URL')

TS_PROJECT_DIR = os.getenv('TS_PROJECT_DIR')
TS_SCRIPT_DIR = os.getenv('TS_SCRIPT_DIR')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'db.sqlite3')

TORTOISE_ORM = {
    "connections": {"default": f'sqlite://{DB_PATH}'},
    "apps": {
        "models": {
            "models": [
                "bot.models.user_models",
                "bot.models.callback_models",
                "bot.models.channel_group_models",
                "aerich.models"
            ],
            "default_connection": "default",
        },
    }
}
