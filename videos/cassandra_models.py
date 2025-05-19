# cassandra_models.py
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
from cassandra.util import uuid_from_time
from datetime import datetime

class UserVideoPlayback(Model):
    __keyspace__ = 'your_keyspace'  # set this to your keyspace

    user_id = columns.UUID(partition_key=True)
    video_id = columns.UUID(primary_key=True)
    playback_time = columns.Double()
    updated_at = columns.DateTime(default=datetime.utcnow)
