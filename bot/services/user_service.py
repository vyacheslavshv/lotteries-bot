from bot.models.user_models import User
from tortoise.exceptions import DoesNotExist


class UserService:
    async def get_or_create_user(self, event):
        user, created = await User.get_or_create(id=event.sender_id)

        # Update user details
        user.name = event.sender.first_name + " " + (event.sender.last_name or "")
        user.username = event.sender.username
        await user.save()

        return user

    async def is_user_banned(self, user_id):
        try:
            user = await User.get(id=user_id)
            return user.is_banned
        except DoesNotExist:
            return False
