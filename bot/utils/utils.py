from telethon.tl.custom import Button
from bot.templates.messages import WELCOME_MESSAGE
from bot.config import BOT_CHANNEL


async def send_welcome_message(event, user, edit=False):
    buttons = [
        [Button.inline("My wallet 💳", "balance")],
        [Button.inline("Share link 🔗", "link")],
        [Button.inline("Guides ℹ️", "guides"),
         Button.url("Updates 📣", f"https://t.me/{BOT_CHANNEL}")],
    ]

    message = WELCOME_MESSAGE.format(name=user.name, balance=user.balance)

    if edit:
        await event.edit(message, buttons=buttons)
    else:
        await event.respond(message, buttons=buttons)
