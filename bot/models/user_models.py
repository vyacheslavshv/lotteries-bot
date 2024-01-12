from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.BigIntField(pk=True)
    name = fields.TextField()
    username = fields.TextField(null=True)
    date = fields.DateField()
    balance = fields.DecimalField(max_digits=11, decimal_places=2, default=0.0)
    referred_by = fields.ForeignKeyField('models.User', related_name='referrals', null=True)
    is_admin = fields.BooleanField(default=False)
    is_banned = fields.BooleanField(default=False)

    # Backward FK relation
    referrals = fields.ReverseRelation['User']
