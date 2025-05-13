from django.db import models

# Create your models here.
class Suggestion(models.Model):
    name = models.CharField(max_length=100, blank=True)
    spotify_url = models.CharField(max_length=100, blank=True)
    # date = models.DateTimeField(auto_now=True)
    # listeners = models.CharField(max_length=100, blank=True)
