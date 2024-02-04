from telethon import events
from telethon.tl.custom import Button
from bot.templates.messages import *
from bot.config import BOT_NAME


async def guides(event):
    buttons = [
        [Button.inline('How it works? 🧑‍💻', 'how_it_works')],
        [Button.inline('How much do you earn? 💰', 'how_much_earn')],
        [Button.inline('How to withdraw from the balance? 💳', 'how_to_withdraw')],
        [Button.inline("What's on the agenda? 🏖", 'whats_on_agenda')],
        [Button.inline('« Back', 'menu')],
    ]
    await event.edit("Some useful guides:", buttons=buttons)


async def how_it_works(event):
    buttons = [
        [Button.inline('« Back', 'guides')],
    ]
    await event.edit(HOW_IT_WORKS_MESSAGE.format(bot_name=BOT_NAME), buttons=buttons)


async def how_much_earn(event):
    buttons = [
        [Button.inline('« Back', 'guides')],
    ]
    await event.edit(HOW_MUCH_EARN_MESSAGE, buttons=buttons)


async def how_to_withdraw(event):
    buttons = [
        [Button.inline('« Back', 'guides')],
    ]
    await event.edit(HOW_TO_WITHDRAW_MESSAGE, buttons=buttons)


async def whats_on_agenda(event):
    buttons = [
        [Button.inline('« Back', 'guides')],
    ]
    await event.edit(WHATS_ON_AGENDA_MESSAGE, buttons=buttons)


def setup_guides_handlers(client):
    @client.on(events.CallbackQuery(data=b'guides'))
    async def handle_guides(event):
        await guides(event)

    @client.on(events.CallbackQuery(data=b'how_it_works'))
    async def handle_how_it_works(event):
        await how_it_works(event)

    @client.on(events.CallbackQuery(data=b'how_much_earn'))
    async def handle_how_much_earn(event):
        await how_much_earn(event)

    @client.on(events.CallbackQuery(data=b'how_to_withdraw'))
    async def handle_how_to_withdraw(event):
        await how_to_withdraw(event)

    @client.on(events.CallbackQuery(data=b'whats_on_agenda'))
    async def handle_whats_on_agenda(event):
        await whats_on_agenda(event)
