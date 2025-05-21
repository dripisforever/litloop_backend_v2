from django.db import models
from users.models import User


class WatchlistItem(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    title    = models.CharField(max_length=255)
    year     = models.CharField(max_length=10, blank=True, null=True)
    imdb_url = models.URLField(blank=True, null=True)



class Movie(models.Model):
    title       = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    movie_file  = models.CharField(max_length=400, null=True)
    hls_file    = models.CharField(max_length=400, null=True)
    poster      = models.CharField(max_length=400, null=True)

    views       = models.IntegerField(default=0)
    impressions = models.IntegerField(default=0)

    tmdb_id     = models.IntegerField(null=True, blank=True)
    imdb_id     = models.IntegerField(null=True, blank=True)


class MovieImpression(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user  = models.ForeignKey('users.User', on_delete=models.CASCADE)


class MovieView(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user  = models.ForeignKey('users.User', on_delete=models.CASCADE)
