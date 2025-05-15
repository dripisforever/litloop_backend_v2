# https://chatgpt.com/c/6820fff4-a0c8-800c-a62c-cb439fe9d552
from uuid import uuid4
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
from datetime import datetime

# ===== Like ===== #
class PostLike(Model):
    __keyspace__ = 'your_keyspace_name'

    post_id   = columns.UUID(partition_key=True)
    user_id   = columns.UUID(primary_key=True)
    liked_at  = columns.DateTime(default=datetime.utcnow)
    username = columns.Text()
    avatar_url = columns.Text()

class PostLikeCounter(Model):
    __keyspace__ = 'your_keyspace_name'

    post_id = columns.UUID(primary_key=True)
    count = columns.Integer()



# ===== Views ===== #
class PostView(Model):
    __keyspace__ = 'your_keyspace_name'

    post_id   = columns.UUID(partition_key=True)
    user_id   = columns.UUID(primary_key=True)
    viewed_at = columns.DateTime(default=datetime.utcnow)
    username = columns.Text()
    avatar_url = columns.Text()

class PostViewCount(Model):
    __keyspace__ = 'your_keyspace_name'

    post_id = columns.UUID(primary_key=True)
    count = columns.Integer()
