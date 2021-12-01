from tortoise.models import Model
from tortoise import fields


class GuildConfig(Model):
    ID = fields.BigIntField(pk=True, unique=True, nullable=False)
    prefix = fields.TextField(default="H!")
    welcome_enabled = fields.BooleanField(default=False)
    leave_enabled = fields.BooleanField(default=False)


class WelcomeConfig(Model):
    ID = fields.BigIntField(pk=True, unique=True, nullable=False)
    channel_id = fields.BigIntField(unique=True, nullable=False)
    message = fields.TextField()


class LeaveConfig(Model):
    ID = fields.BigIntField(pk=True, unique=True, nullable=False)
    channel_id = fields.BigIntField(unique=True, nullable=False)
    message = fields.TextField()


class Servers(Model):
    rID = fields.BigIntField(pk=True, unique=True, nullable=False)
    id = fields.TextField()
    Server_Name = fields.TextField()
    Server_ID = fields.BigIntField()
    Member_Count = fields.BigIntField()
    Channels = fields.BigIntField()
    Last_Update = fields.DatetimeField()