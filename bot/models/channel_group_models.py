import uuid
from tortoise.models import Model
from tortoise import fields


class ChannelGroup(Model):
    id = fields.BigIntField(pk=True)
    name = fields.TextField()
    url = fields.TextField()

    class Meta:
        table = "channel_group"


class UserChannelGroup(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    user = fields.ForeignKeyField('models.User', related_name='subscriptions')
    channel_group = fields.ForeignKeyField('models.ChannelGroup', related_name='subscribers')

    class Meta:
        table = "user_channel_group"
