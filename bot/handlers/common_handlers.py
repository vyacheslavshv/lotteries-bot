from bot.config import BOT_NAME
from bot.services.user_service import UserService
from bot.templates.messages import *
from bot.handlers.message_handlers import welcome_message
from telethon.tl.custom import Button
from telethon import events
from datetime import datetime
from bot.models import ChannelGroup, UserChannelGroup
from bot.utils.utils import check_user_membership


async def link(event):
    user_service = UserService(event)
    user = await user_service.get_user()

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


async def attendance_check(event):
    now = datetime.utcnow()
    allowed_intervals = [
        (datetime(now.year, now.month, now.day, 10, 0),
         datetime(now.year, now.month, now.day, 15, 0)),
        (datetime(now.year, now.month, now.day, 16, 0),
         datetime(now.year, now.month, now.day, 19, 0)),
        (datetime(now.year, now.month, now.day, 20, 0),
         datetime(now.year, now.month, now.day, 23, 0)),
    ]

    if any(start <= now <= end for start, end in allowed_intervals):
        user_service = UserService(event)
        user = await user_service.get_user()
        user.balance += 3
        await user.save()
        await event.answer("Thank you for checking in. You've received 3 additional points.", alert=True)
        await welcome_message(event)
    else:
        await event.answer(ATTENDANCE_CHECK_MESSAGE, alert=True)


async def join_channels(event):
    buttons = []
    channels_groups = await ChannelGroup.all()
    for channel_group in channels_groups:
        subscription_exists = await UserChannelGroup.filter(
            user_id=event.sender_id, channel_group=channel_group
        ).exists()
        if not subscription_exists:
            buttons.append([Button.url(channel_group.name, f'https://t.me/{channel_group.url}')])

    buttons.append([Button.inline("« Back", "menu")])
    if len(buttons) > 1:
        buttons[-1].append(Button.inline("Check joining ✅", "check_joining"))

    await event.edit("Join channels or groups below and receive 10 points for each 🥳", buttons=buttons)


async def check_joining(event):
    user_service = UserService(event)
    user = await user_service.get_user()
    points_awarded = 0

    channels_groups = await ChannelGroup.all()
    for channel_group in channels_groups:
        member = await check_user_membership(event, channel_group.id, user.id)
        if member:
            subscription_exists = await UserChannelGroup.filter(
                user_id=user.id, channel_group=channel_group
            ).exists()
            if not subscription_exists:
                await UserChannelGroup.create(user=user, channel_group=channel_group)
                points_awarded += 10

    if points_awarded > 0:
        user.balance += points_awarded
        await user.save()
        await event.answer(f"You've been awarded {points_awarded} points for joining new channels/groups!", alert=True)
    else:
        await event.answer(
            "No new subscriptions detected or unable to verify. Make sure you've joined the channels/groups.",
            alert=True
        )
    await join_channels(event)


def setup_common_handlers(client):
    @client.on(events.CallbackQuery(data=b'menu'))
    async def handle_menu(event):
        await welcome_message(event)

    @client.on(events.CallbackQuery(data=b'link'))
    async def handle_link(event):
        await link(event)

    @client.on(events.CallbackQuery(data=b'attendance_check'))
    async def handle_attendance_check(event):
        await attendance_check(event)

    @client.on(events.CallbackQuery(data=b'join_channels'))
    async def handle_join_channels(event):
        await join_channels(event)

    @client.on(events.CallbackQuery(data=b'check_joining'))
    async def handle_check_joining(event):
        await check_joining(event)
