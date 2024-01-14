import asyncio

from asyncio import CancelledError
from tortoise import Tortoise
from telethon import TelegramClient
from bot.config import API_ID, API_HASH, BOT_TOKEN, TORTOISE_ORM
from bot.handlers.message_handlers import setup_message_handlers
from bot.handlers.common_handlers import setup_common_handlers
from bot.handlers.guides.guides_hundlers import setup_guides_handlers


async def main():
    # Initialize Tortoise ORM
    await Tortoise.init(TORTOISE_ORM)

    client = TelegramClient('data/bot', API_ID, API_HASH)

    await client.start(bot_token=BOT_TOKEN)

    setup_message_handlers(client)
    setup_common_handlers(client)
    setup_guides_handlers(client)

    try:
        await client.run_until_disconnected()
    except CancelledError:
        pass
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
