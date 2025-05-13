# https://chatgpt.com/c/6820fff4-a0c8-800c-a62c-cb439fe9d552
from uuid import uuid4
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
from datetime import datetime


class Post(Model):
    __keyspace__ = 'your_keyspace_name'

    user_id     = columns.UUID(partition_key=True)
    post_id     = columns.UUID(primary_key=True, default=uuid4)

    title       = columns.Text()
    description = columns.Text()
    caption     = columns.Text()
    image       = columns.Text()
    friendly_id = columns.Text(index=True)

    created_at  = columns.DateTime(default=datetime.utcnow)
    updated_at  = columns.DateTime(default=datetime.utcnow)

    photo_ids     = columns.List(columns.UUID)
    video_ids     = columns.List(columns.UUID)
    track_ids     = columns.List(columns.UUID)
    playlist_ids  = columns.List(columns.UUID)

    like_user_ids       = columns.Set(columns.UUID)
    dislike_user_ids    = columns.Set(columns.UUID)
    view_user_ids       = columns.Set(columns.UUID)
    impression_user_ids = columns.Set(columns.UUID)


class PostMediaItem(Model):
    __keyspace__ = 'your_keyspace_name'

    post_id    = columns.UUID(partition_key=True)
    media_type = columns.Text(primary_key=True)  # 'photo', 'video', etc.
    ordering   = columns.Integer(primary_key=True)
    media_id   = columns.UUID()

class PostByFriendlyId(Model):
    __keyspace__ = 'your_keyspace_name'

    friendly_id = columns.Text(primary_key=True)
    post_id     = columns.UUID()
    user_id     = columns.UUID()
    caption     = columns.Text()
    created_at  = columns.DateTime()
