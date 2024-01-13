import asyncio
from tortoise import Tortoise
from telethon import TelegramClient
from telethon.sessions import StringSession
from bot.config import API_ID, API_HASH, BOT_SESSION, TORTOISE_ORM
from bot.handlers.message_handlers import setup_message_handlers
from bot.handlers.common_handlers import setup_common_handlers
from bot.handlers.guides.guides_hundlers import setup_guides_handlers



async def main():
    # Initialize Tortoise ORM
    await Tortoise.init(TORTOISE_ORM)

    async with TelegramClient(StringSession(BOT_SESSION), API_ID, API_HASH) as client:

        setup_message_handlers(client)
        setup_common_handlers(client)
        setup_guides_handlers(client)

        await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        exit()
