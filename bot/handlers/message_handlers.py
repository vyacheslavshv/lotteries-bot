from telethon import events


def message_handlers(client):
    @client.on(events.NewMessage())
    async def any_message(event):
        await event.respond('Welcome to the Lottery Bot!')
