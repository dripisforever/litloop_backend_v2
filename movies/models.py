from django.db import models
from users.models import User

# Create your models here.
class Movie(models.Model):
    tmdb_id = models.IntegerField(null=True, blank=True)
    imdb_id = models.IntegerField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    movie_file = models.FileField(upload_to='uploaded_media/movie', null=True, blank=True)
    poster = models.FileField(upload_to='uploaded_media/movie/poster', null=True, blank=True)

    views = models.ManyToManyField(User, through='MovieView', blank=True, related_name='movie_views')
    impressions = models.ManyToManyField(User, through='MovieImpression', blank=True, related_name='movie_impressions')

    

class MovieImpression(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

class MovieView(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
