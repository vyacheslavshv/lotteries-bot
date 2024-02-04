import asyncio

from asyncio import CancelledError
from tortoise import Tortoise
from telethon import TelegramClient
from bot.config import API_ID, API_HASH, BOT_TOKEN, TORTOISE_ORM
from bot.handlers.message_handlers import setup_message_handlers
from bot.handlers.common_handlers import setup_common_handlers
from bot.handlers.guides_handlers import setup_guides_handlers
from bot.handlers.wallet_handlers import setup_wallet_handlers

from bot.tasks.monthly_withdrawals import process_monthly_withdrawals
from bot.tasks.delete_callbacks import delete_old_callback_data
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import utc

from datetime import datetime


async def start_schedulers(client):
    scheduler = AsyncIOScheduler(timezone=utc)
    scheduler.add_job(
        process_monthly_withdrawals,
        CronTrigger(day=1, hour=0, minute=0),
        (client,),
        next_run_time=datetime.utcnow()
    )
    scheduler.add_job(
        delete_old_callback_data,
        CronTrigger(hour=0, minute=0)
    )
    scheduler.start()


async def main():
    # Initialize Tortoise ORM
    await Tortoise.init(TORTOISE_ORM)

    client = TelegramClient('data/bot', API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)

    setup_message_handlers(client)
    setup_common_handlers(client)
    setup_guides_handlers(client)
    setup_wallet_handlers(client)

    # Start schedulers
    await start_schedulers(client)

    try:
        await client.run_until_disconnected()
    except CancelledError:
        pass
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
