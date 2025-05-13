from django.apps import apps
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.sites.shortcuts import get_current_site

from artists.models import Artist
from tracks.models import Track
from images.models import Image
from albums.managers import AlbumManager, SpotifyAlbumManager


class AlbumTrack(models.Model):
    pass

class AlbumArtist(models.Model):
    album  = models.ForeignKey('albums.Album', on_delete=models.CASCADE)
    artist = models.ForeignKey('artists.Artist', on_delete=models.CASCADE)
    role   = models.CharField(max_length=200)

class AlbumLike(models.Model):
    album = models.ForeignKey('albums.Album', on_delete=models.CASCADE)
    liked_by = models.ForeignKey('users.User', on_delete=models.CASCADE)

class AlbumDislike(models.Model):
    album = models.ForeignKey('albums.Album', on_delete=models.CASCADE)
    dislike_by = models.ForeignKey('users.User', on_delete=models.CASCADE)

class AlbumImpression(models.Model):
    album = models.ForeignKey('albums.Album', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

class AlbumView(models.Model):
    album = models.ForeignKey('albums.Album', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)



class Album(models.Model):
    id         = models.BigAutoField(primary_key=True)
    name       = models.CharField(max_length=400)
    album_uri  = models.CharField(max_length=400)
    artists    = models.ManyToManyField('artists.Artist', related_name='albums', through=AlbumArtist)
    # images  = models.ManyToManyField(Image, related_name='albums')
    # likes   = models.ManyToManyField('users.User', related_name='liked_albums', blank=True, through=AlbumLike)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # tracks = ManyToManyField(Track,  through='AlbumTracks', related_name='album_tracks')
    # author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    objects = AlbumManager()

# class SpotifyAlbum(models.Model):
#     id         = models.BigAutoField(primary_key=True)
#     name       = models.CharField(max_length=400)
#     album_uri  = models.CharField(max_length=400)
#     artists    = models.ManyToManyField('artists.SpotigyArtist', related_name='albums', through=SpotifyAlbumArtist)
#     # images  = models.ManyToManyField(Image, related_name='albums')
#     # likes   = models.ManyToManyField('users.User', related_name='liked_albums', blank=True, through=AlbumLike)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     # tracks = ManyToManyField(Track,  through='AlbumTracks', related_name='album_tracks')
#     # author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
#     objects = SpotifyAlbumManager()


# import artists.models as Artist
# import tracks.models as Track
# import images.models as Image
# import likes.models  as Like

# Track = apps.get_model(app_label='tracks', model_name='Track')
# Artist = apps.get_model(app_label='artists', model_name='Artist')
# Album = apps.get_model(app_label='albums', model_name='Album')
# Like = apps.get_model(app_label='likes', model_name='Like')
