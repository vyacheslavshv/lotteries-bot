from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.BigIntField(pk=True)
    name = fields.TextField(null=True)
    username = fields.TextField(null=True)
    last_activity = fields.DatetimeField(auto_now=True)
    balance = fields.IntField(default=0)
    wallet_address = fields.TextField(null=True)
    referred_by = fields.ForeignKeyField('models.User', related_name='referrals', null=True)
    is_admin = fields.BooleanField(default=False)
    is_banned = fields.BooleanField(default=False)
    withdraw_request = fields.BooleanField(default=False)

    captcha_passed = fields.BooleanField(default=False)
    emoji_passed = fields.BooleanField(default=False)
    data = fields.TextField(null=True)

    # Backward FK relation
    referrals = fields.ReverseRelation['User']

    class Meta:
        table = "user"
