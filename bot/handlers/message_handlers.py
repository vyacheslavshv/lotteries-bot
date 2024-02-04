from telethon import events
from tortoise.exceptions import DoesNotExist
from bot.templates.messages import *
from bot.templates.buttons import *
from bot.services.user_service import UserService
from bot.services.captcha_service import CaptchaService
from bot.models import User


async def welcome_message(event, edit=True):
    user_service = UserService(event)
    user = await user_service.get_user()

    if user.referred_by:
        if not user.captcha_passed:
            passed = False
            if user.data and user.data == event.message.text:
                passed = True

                user.captcha_passed = True
                user.emoji_passed = True  # Temporally

                user.balance += 15
                user.data = None
                await user.save()

                referrer = await User.filter(id=user.referred_by_id).first()
                if referrer:
                    points_for_referrer = 15
                    referrer.balance += points_for_referrer
                    await referrer.save()
                    await event.client.send_message(
                        referrer.id,
                        f"You are awarded {points_for_referrer} points for "
                        f"the invited user: {user.name}"
                    )

            if not passed:
                captcha_service = CaptchaService(event)
                image_bytes, code = await captcha_service.generate_captcha()
                uploaded_file = await event.client.upload_file(file=image_bytes, file_name="captcha.png")

                user.data = code
                await user.save()

                await event.respond(
                    "Confirm that you are not a robot, enter the numbers from the captcha.",
                    file=uploaded_file
                )
                return

        if not user.emoji_passed:
            pass

    message = WELCOME_MESSAGE.format(name=user.name, balance=user.balance)
    if edit:
        await event.edit(message, buttons=MENU_BUTTONS)
    else:
        await event.respond(message, buttons=MENU_BUTTONS)


async def new_referral(event, referred_by):
    user_service = UserService(event)
    user, created = await user_service.get_user(return_created=True)

    if created and referred_by:
        try:
            referrer = await User.get(id=int(referred_by))
            user.referred_by = referrer
            await user.save()
        except (DoesNotExist, ValueError):
            pass

    await welcome_message(event, edit=False)


def setup_message_handlers(client):
    @client.on(events.NewMessage())
    async def handle_any_message(event):
        text = event.message.text
        command = "/start "
        if text.startswith(command):
            await new_referral(event, text[len(command):])
            return
        await welcome_message(event, edit=False)
