from bot.config import BOT_NAME
from telethon import events
from bot.utils.utils import send_welcome_message
from bot.services.user_service import UserService
from bot.templates.messages import *
from telethon.tl.custom import Button


def setup_common_handlers(client):
    @client.on(events.CallbackQuery(data=b'menu'))
    async def handle_menu_query(event):
        user_service = UserService()
        user = await user_service.get_or_create_user(event)
        await send_welcome_message(event, user, edit=True)

    @client.on(events.CallbackQuery(data=b'balance'))
    async def handle_balance_query(event):
        user_service = UserService()
        user = await user_service.get_or_create_user(event)

        buttons = [
            [Button.inline('Withdraw money 💰', 'withdraw')],
            [Button.inline('« Back', 'menu')],
        ]
        await event.edit(
            BALANCE_MESSAGE.format(name=user.name, balance=user.balance),
            buttons=buttons
        )

    @client.on(events.CallbackQuery(data=b'withdraw'))
    async def handle_withdraw_query(event):
        user_service = UserService()
        user = await user_service.get_or_create_user(event)

        if user.balance < 100:
            await event.answer(
                "You do not have enough money in your account, "
                "in order to withdraw money you must reach $100.",
                alert=True
            )
            return

        buttons = [
            [Button.inline('« Back', 'balance')]
        ]

        await event.edit(
            WITHDRAW_MESSAGE.format(user.name, user.balance),
            buttons=buttons
        )

    @client.on(events.CallbackQuery(data=b'link'))
    async def handle_link_query(event):
        user_service = UserService()
        user = await user_service.get_or_create_user(event)

        buttons = [
            [Button.url(
                'Share on WhatsApp 📱',
                f'https://api.whatsapp.com/send?text=https://t.me/{BOT_NAME}?start={user.id}'
            )],
            [Button.url(
                'Share on Telegram ✉️',
                f'https://t.me/share/url?url=https://t.me/{BOT_NAME}?start={user.id}'
            )],
            [Button.url(
                'Share on Facebook 📷',
                f'https://www.facebook.com/sharer.php?u=https://t.me/{BOT_NAME}?start={user.id}'
            )],
            [Button.inline('« Back', 'menu')],
        ]

        await event.edit(
            PERSONAL_LINK_MESSAGE.format(
                name=user.name, bot_name=BOT_NAME, user_id=user.id
            ),
            buttons=buttons
        )
