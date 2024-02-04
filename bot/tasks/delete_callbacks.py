from datetime import datetime, timedelta
from bot.models import CallbackData
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)


async def delete_old_callback_data():
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    old_data = await CallbackData.filter(created_at__lt=cutoff_date)
    await CallbackData.filter(id__in=[data.id for data in old_data]).delete()

    logger.info(f"Deleted old callback data created before {cutoff_date}")
