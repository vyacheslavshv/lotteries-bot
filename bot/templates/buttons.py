from telethon.tl.custom import Button
from bot.config import BOT_CHANNEL

BALANCE_BUTTON = Button.inline('« Back', 'balance')

MENU_BUTTONS = [
    [Button.inline("Share link 🔗", "link"),
     Button.inline("My wallet 💳", "balance")],
    [Button.inline("More money 💰", "join_channels"),
     Button.inline("Attendance check 🟢", "attendance_check")],
    [Button.inline("Guides ℹ️", "guides"),
     Button.url("Updates 📣", f"https://t.me/{BOT_CHANNEL}")],
]
