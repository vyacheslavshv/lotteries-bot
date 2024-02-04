from bot.models import User


class UserService:
    def __init__(self, event):
        self.event = event

    async def get_user(self, return_created=False):
        user, created = await User.get_or_create(id=self.event.sender_id)

        current_name = self.event.sender.first_name + " " + (self.event.sender.last_name or "")
        current_username = self.event.sender.username

        if user.name != current_name:
            user.name = current_name
        if user.username != current_username:
            user.username = current_username
        await user.save()

        if return_created:
            return user, created
        return user
