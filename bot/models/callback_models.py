import uuid
from tortoise.models import Model
from tortoise import fields


class CallbackData(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    data = fields.JSONField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "callback_data"
