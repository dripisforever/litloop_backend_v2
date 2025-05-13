from django.db import models
from artists.models import Artist
from tracks.models import Track
from images.models import Image

class ArtistManager(models.Manager):    
    def create(cls, **kwargs):
        from artists.models import Artist
        from albums.models import Album
        from tracks.models import Track
        from images.models import Image

        artist, created = cls.objects.get_or_create(
            artist_uri = kwargs['id'],
            name = kwargs['name']
        )

        # for track_data in kwargs['tracks']:
        #
        #     track, created = Track.objects.get_or_create(
        #         artist_uri = artists_data["id"],
        #         name = artists_data["name"]
        #
        #     )
        #     artist.tracks.add(artist)
        #
        # for album_data in kwargs['album']:
        #
        #     album, created = Album.objects.get_or_create(
        #         album_uri = album_data["id"],
        #         name = album_data["name"]
        #
        #     )
        #     artist.albums.add(album)

        for images_data in kwargs['images']:
            # extract_id_from_url = images_data["url"]
            image, created = Image.objects.get_or_create(
                url = images_data["url"],
                height = images_data["height"],
                width = images_data["width"],
                artist_id = artist.id,
            )

        #
        return artist
