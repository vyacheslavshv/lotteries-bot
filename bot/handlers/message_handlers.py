from telethon import events
from telethon.tl.custom import Button
from bot.templates.messages import WELCOME_MESSAGE
from bot.services.user_service import UserService
from bot.utils.utils import send_welcome_message


def setup_message_handlers(client):
    @client.on(events.NewMessage())
    async def welcome_message(event):
        user_service = UserService()

        # Get or create user in the database and update details
        user = await user_service.get_or_create_user(event)

        # Check if user is banned
        if await user_service.is_user_banned(event.sender_id):
            return

        # Respond with welcome message
        await send_welcome_message(event, user, edit=False)
