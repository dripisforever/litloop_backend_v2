# https://chatgpt.com/c/6820fff4-a0c8-800c-a62c-cb439fe9d552
from uuid import uuid4
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
from datetime import datetime

class Message(Model):
    __keyspace__ = 'your_keyspace_name'

    group_id     = columns.UUID(partition_key=True)
    message_id   = columns.UUID(primary_key=True, default=uuid4)

    sender_id    = columns.UUID()
    message_text = columns.Text()
    date_posted  = columns.DateTime(default=datetime.utcnow)

    video_ids    = columns.List(columns.UUID)
    photo_ids    = columns.List(columns.UUID)
    track_ids    = columns.List(columns.UUID)
    attachment_ids = columns.List(columns.UUID)

class GroupChat(Model):
    __keyspace__ = 'your_keyspace_name'

    group_id    = columns.UUID(primary_key=True, default=uuid4)
    name        = columns.Text()
    description = columns.Text()
    member_ids  = columns.Set(columns.UUID)
