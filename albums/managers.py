from django.db import models
from artists.models import Artist
from tracks.models import Track
from images.models import Image

class AlbumManager(models.Manager):
    def create_album(self, **kwargs):
        album, created = self.get_or_create(
            album_uri=kwargs['id'],
            name=kwargs['name'],
        )

        for artist_data in kwargs['artists']:
            artist, _ = Artist.objects.get_or_create(
                artist_uri=artist_data['id'],
                name=artist_data['name'],
            )
            album.artists.add(artist)

        for track_data in kwargs['tracks']['items']:
            track, _ = Track.objects.get_or_create(
                track_uri=track_data["id"],
                name=track_data["name"],
                album_id=album.id,
                track_number=track_data['track_number'],
            )
            album.tracks.add(track)

            for artist_data in track_data['artists']:
                artist, _ = Artist.objects.get_or_create(
                    artist_uri=artist_data['id'],
                    name=artist_data['name'],
                )
                track.artists.add(artist)

        for images_data in kwargs['images']:
            Image.objects.get_or_create(
                url=images_data["url"],
                height=images_data["height"],
                width=images_data["width"],
                album_id=album.id,
            )

        return album


class SpotifyAlbumManager(models.Manager):
    def create_album(self, **kwargs):
        album, created = self.get_or_create(
            album_uri=kwargs['id'],
            name=kwargs['name'],
        )

        for artist_data in kwargs['artists']:
            artist, _ = Artist.objects.get_or_create(
                artist_uri=artist_data['id'],
                name=artist_data['name'],
            )
            album.artists.add(artist)

        for track_data in kwargs['tracks']['items']:
            track, _ = Track.objects.get_or_create(
                track_uri=track_data["id"],
                name=track_data["name"],
                album_id=album.id,
                track_number=track_data['track_number'],
            )
            album.tracks.add(track)

            for artist_data in track_data['artists']:
                artist, _ = Artist.objects.get_or_create(
                    artist_uri=artist_data['id'],
                    name=artist_data['name'],
                )
                track.artists.add(artist)

        for images_data in kwargs['images']:
            Image.objects.get_or_create(
                url=images_data["url"],
                height=images_data["height"],
                width=images_data["width"],
                album_id=album.id,
            )

        return album
