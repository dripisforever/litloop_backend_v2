from django.apps import apps
from django.db import models
# from django.contrib.contenttypes.fields import GenericRelation



class Artist(models.Model):
    name = models.CharField(max_length=300)
    artist_uri = models.CharField(max_length=300)
    # album = models.ManyToManyField(Album, related_name='artists')
    # albums = models.ManyToManyField('albums.Album', related_name='artists')
    # album = models.ManyToManyField('albums.Album', related_name='artists', on_delete=models.CASCADE)
    # track = models.ManyToManyField(Track, related_name='artists')
    # tracks = models.ManyToManyField('tracks.Track', related_name='artists')
    # track = models.ManyToManyField('tracks.Track', related_name='artists', on_delete=models.CASCADE)
    # images = models.ManyToManyField(Image, related_name='artists')

    

# from albums.models import Album
# from tracks.models import Track

# import albums.models as Album
# import tracks.models as Track

# Track = apps.get_model(app_label='tracks', model_name='Track')
# Artist = apps.get_model(app_label='artists', model_name='Artist')
# Album = apps.get_model(app_label='albums', model_name='Album')
# Like = apps.get_model(app_label='likes', model_name='Like')
