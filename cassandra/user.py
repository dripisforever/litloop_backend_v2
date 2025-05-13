# https://chatgpt.com/c/6820fff4-a0c8-800c-a62c-cb439fe9d552
from uuid import uuid4
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
from datetime import datetime

class User(Model):
    __keyspace__ = 'your_keyspace_name'

    user_id    = columns.UUID(primary_key=True, default=uuid4)
    username   = columns.Text(index=True)
    email      = columns.Text(index=True)
    avatar     = columns.Text()

    is_verified = columns.Boolean()
    is_active   = columns.Boolean()
    is_staff    = columns.Boolean()

    created_at  = columns.DateTime(default=datetime.utcnow)
    updated_at  = columns.DateTime(default=datetime.utcnow)


class Follow(Model):
    __keyspace__ = 'your_keyspace_name'

    follower_id  = columns.UUID(partition_key=True)
    following_id = columns.UUID(primary_key=True)
    created_at   = columns.DateTime(default=datetime.utcnow)
