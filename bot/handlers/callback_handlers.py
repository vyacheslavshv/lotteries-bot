from telethon import events


def callback_handlers(client):
    @client.on(events.CallbackQuery(data=b'some_callback_data'))
    async def handle_callback(event):
        # Handle the callback query here...
        await event.answer('Callback received!')
