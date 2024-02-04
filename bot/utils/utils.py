from bot.utils.logger import setup_logger
from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

logger = setup_logger(__name__)


async def check_user_membership(event, channel_id, user_id):
    try:
        await event.client(GetParticipantRequest(channel_id, user_id))
        return True
    except UserNotParticipantError:
        return False
    except Exception as e:
        logger.error(f"Error checking membership for user {user_id} in {channel_id}: {e}", exc_info=True)
        return False
