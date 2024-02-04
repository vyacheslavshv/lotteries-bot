import uuid
import asyncio

from telethon import events
from pytonconnect import TonConnect
from pytoniq_core import Address

from bot.config import MANIFEST_URL
from bot.models import CallbackData
from bot.services.user_service import UserService
from bot.templates.messages import *
from bot.templates.buttons import *


async def balance(event):
    user_service = UserService(event)
    user = await user_service.get_user()

    if user.wallet_address:
        wallet_button = [Button.inline('Disconnect wallet ❌', 'disconnect_wallet')]
    else:
        wallet_button = [Button.inline('Connect wallet ✅', 'wallets_list')]

    buttons = [
        wallet_button,
        [Button.inline('Withdraw money 💰', 'withdraw')],
        [Button.inline('« Back', 'menu')],
    ]
    await event.edit(
        BALANCE_MESSAGE.format(
            name=user.name, balance=user.balance,
            wallet_address=user.wallet_address
            if user.wallet_address else 'not connected ❌'
        ),
        buttons=buttons
    )


async def withdraw(event):
    user_service = UserService(event)
    user = await user_service.get_user()

    if not user.wallet_address:
        await event.answer(
            "You have not connected or disconnected "
            "your wallet. Plug it in first!",
            alert=True
        )
    elif user.withdraw_request:
        await event.answer(WITHDRAW_MESSAGE, alert=True)
    elif user.balance < 1500:
        await event.answer(
            "You do not have enough money in your account, "
            "in order to withdraw money you must reach 1500 points.",
            alert=True
        )
    else:
        user.withdraw_request = True
        await user.save()

        await event.answer(WITHDRAW_MESSAGE, alert=True)


async def wallets_list(event):
    buttons = []

    wallets = TonConnect.get_wallets()
    for wallet in wallets:
        unique_id = str(uuid.uuid4())
        callback_data = {'wallet_name': wallet['name']}
        await CallbackData.create(id=unique_id, data=callback_data)

        buttons.append([Button.inline(wallet['name'], f'wallet_url:{unique_id}')])

    buttons.append([BALANCE_BUTTON])
    await event.edit('Choose wallet to connect', buttons=buttons)


async def wallet_url(event):
    unique_id = event.data.decode('utf-8').split(':')[1]
    callback = await CallbackData.filter(id=unique_id).first()
    if not callback:
        await event.answer(EXPIRED_LINK_MESSAGE, alert=True)
        return

    connector = TonConnect(MANIFEST_URL)
    wallet_name = callback.data['wallet_name']
    wallets = connector.get_wallets()
    wallet = None

    for w in wallets:
        if w['name'] == wallet_name:
            wallet = w

    generated_url = await connector.connect(wallet)

    buttons = [
        [Button.url("Connect ✅", generated_url)],
        [Button.inline('« Back', 'wallets_list')]
    ]

    await event.edit(f'Connect "{wallet_name}" within 3 minutes', buttons=buttons)

    for i in range(1, 180):
        await asyncio.sleep(1)
        if connector.connected:
            if connector.account.address:
                user_service = UserService(event)
                user = await user_service.get_user()
                wallet_address = connector.account.address
                wallet_address = Address(wallet_address).to_str(is_bounceable=False)
                user.wallet_address = wallet_address
                await user.save()

                await event.edit(
                    f'You are connected with address: `{wallet_address}`',
                    buttons=[[BALANCE_BUTTON]]
                )
                return

    await event.edit(f'Timeout error on wallet connection!', buttons=[[BALANCE_BUTTON]])


async def disconnect_wallet(event):
    user_service = UserService(event)
    user = await user_service.get_user()
    user.wallet_address = None
    await user.save()

    await event.answer('Wallet successfully disconnected')
    await balance(event)


def setup_wallet_handlers(client):
    @client.on(events.CallbackQuery(data=b'balance'))
    async def handle_balance(event):
        await balance(event)

    @client.on(events.CallbackQuery(data=b'withdraw'))
    async def handle_withdraw(event):
        await withdraw(event)

    @client.on(events.CallbackQuery(data=b'wallets_list'))
    async def handle_wallets_list(event):
        await wallets_list(event)

    @client.on(events.CallbackQuery(pattern=r'wallet_url:(.*)'))
    async def handle_wallet_url(event):
        await wallet_url(event)

    @client.on(events.CallbackQuery(data=b'disconnect_wallet'))
    async def handle_disconnect_wallet(event):
        await disconnect_wallet(event)
