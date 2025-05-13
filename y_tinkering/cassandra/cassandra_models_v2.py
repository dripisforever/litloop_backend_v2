# cassandra_models.py

from uuid import uuid4
from datetime import datetime
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns


# ========== POSTS ==========

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


class PostLike(Model):
    __keyspace__ = 'your_keyspace_name'
    post_id   = columns.UUID(partition_key=True)
    user_id   = columns.UUID(primary_key=True)
    liked_at  = columns.DateTime(default=datetime.utcnow)


class PostDislike(Model):
    __keyspace__ = 'your_keyspace_name'
    post_id     = columns.UUID(partition_key=True)
    user_id     = columns.UUID(primary_key=True)
    disliked_at = columns.DateTime(default=datetime.utcnow)


class PostView(Model):
    __keyspace__ = 'your_keyspace_name'
    post_id   = columns.UUID(partition_key=True)
    user_id   = columns.UUID(primary_key=True)
    viewed_at = columns.DateTime(default=datetime.utcnow)


class PostImpression(Model):
    __keyspace__ = 'your_keyspace_name'
    post_id       = columns.UUID(partition_key=True)
    user_id       = columns.UUID(primary_key=True)
    impressed_at  = columns.DateTime(default=datetime.utcnow)


class PostMediaItem(Model):
    __keyspace__ = 'your_keyspace_name'
    post_id    = columns.UUID(partition_key=True)
    media_type = columns.Text(primary_key=True)
    ordering   = columns.Integer(primary_key=True)
    media_id   = columns.UUID()


class PostByFriendlyId(Model):
    __keyspace__ = 'your_keyspace_name'
    friendly_id = columns.Text(primary_key=True)
    post_id     = columns.UUID()
    user_id     = columns.UUID()
    caption     = columns.Text()
    created_at  = columns.DateTime()


# ========== VIDEO ==========

class Video(Model):
    __keyspace__ = 'your_keyspace_name'
    video_id     = columns.UUID(primary_key=True, default=uuid4)
    user_id      = columns.UUID(index=True)

    title        = columns.Text()
    description  = columns.Text()
    s3_key       = columns.Text()
    filename     = columns.Text()
    video_file   = columns.Text()
    thumbnail    = columns.Text()
    sprites      = columns.Text()

    created_at   = columns.DateTime(default=datetime.utcnow)


# ========== PHOTO ==========

class Photo(Model):
    __keyspace__ = 'your_keyspace_name'
    photo_id    = columns.UUID(primary_key=True, default=uuid4)
    user_id     = columns.UUID(index=True)

    title       = columns.Text()
    s3_key      = columns.Text()
    filename    = columns.Text()
    photo_file  = columns.Text()

    created_at  = columns.DateTime(default=datetime.utcnow)
    friendly_token = columns.Text(index=True)

    like_user_ids       = columns.Set(columns.UUID)
    dislike_user_ids    = columns.Set(columns.UUID)
    view_user_ids       = columns.Set(columns.UUID)
    impression_user_ids = columns.Set(columns.UUID)


class PhotoAlbum(Model):
    __keyspace__ = 'your_keyspace_name'
    album_id       = columns.UUID(primary_key=True, default=uuid4)
    user_id        = columns.UUID(index=True)

    title          = columns.Text()
    description    = columns.Text()
    photo_ids      = columns.List(columns.UUID)
    friendly_token = columns.Text(index=True)
    created_at     = columns.DateTime(default=datetime.utcnow)


class PhotoAlbumItem(Model):
    __keyspace__ = 'your_keyspace_name'
    album_id     = columns.UUID(partition_key=True)
    ordering     = columns.Integer(primary_key=True)
    photo_id     = columns.UUID()
    action_date  = columns.DateTime(default=datetime.utcnow)


# ========== USER ==========

class User(Model):
    __keyspace__ = 'your_keyspace_name'
    user_id     = columns.UUID(primary_key=True, default=uuid4)

    username    = columns.Text(index=True)
    email       = columns.Text(index=True)
    avatar      = columns.Text()

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


# ========== GROUP CHAT / MESSAGES ==========

class GroupChat(Model):
    __keyspace__ = 'your_keyspace_name'
    group_id    = columns.UUID(primary_key=True, default=uuid4)
    name        = columns.Text()
    description = columns.Text()
    member_ids  = columns.Set(columns.UUID)


class Message(Model):
    __keyspace__ = 'your_keyspace_name'
    group_id     = columns.UUID(partition_key=True)
    message_id   = columns.UUID(primary_key=True, default=uuid4)

    sender_id    = columns.UUID()
    message_text = columns.Text()
    date_posted  = columns.DateTime(default=datetime.utcnow)

    video_ids       = columns.List(columns.UUID)
    photo_ids       = columns.List(columns.UUID)
    track_ids       = columns.List(columns.UUID)
    attachment_ids  = columns.List(columns.UUID)
