from django.db import models
from artists.models import Artist
from images.models import Image

class TrackManager(models.Manager):
    def create(cls, **kwargs):
        from artists.models import Artist
        from albums.models import Album
        from images.models import Image

        album, created = Album.objects.get_or_create(
            album_uri = kwargs['album']['id'],
            name = kwargs['album']['name']

        )

        for album_artists in kwargs['album']['artists']:
            artist, created = Artist.objects.get_or_create(
                artist_uri = album_artists["id"],
                name = album_artists["name"]

            )
            album.artists.add(artist)

        track, created = cls.objects.get_or_create(
            track_uri = kwargs['id'],
            name = kwargs['name'],
            album_id = album.id,
            track_number = kwargs['track_number'],
        )
        # track.album.add(album)
        for artists_data in kwargs['artists']:

            artist, created = Artist.objects.get_or_create(
                artist_uri = artists_data["id"],
                name = artists_data["name"]

            )
            track.artists.add(artist)


        return track
