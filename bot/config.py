import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_SESSION = os.getenv('BOT_SESSION')
BOT_NAME = os.getenv('BOT_NAME')
BOT_CHANNEL = os.getenv('BOT_CHANNEL')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'db.sqlite3')

TORTOISE_ORM = {
    "connections": {"default": f'sqlite://{DB_PATH}'},
    "apps": {
        "models": {
            "models": ["bot.models.user_models", "aerich.models"],
            "default_connection": "default",
        },
    }
}
