from django.apps import apps
from django.db import models
# from django.contrib.contenttypes.fields import GenericRelation



class Artist(models.Model):
    name = models.CharField(max_length=300)
    artist_uri = models.CharField(max_length=300)

    # albums = models.ManyToManyField('albums.Album', related_name='artists')
    # tracks = models.ManyToManyField('tracks.Track', related_name='artists')
    # images = models.ManyToManyField('images.Image', related_name='artists')
