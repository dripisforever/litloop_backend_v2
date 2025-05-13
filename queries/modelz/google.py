from django.db import models

# Create your models here.
class GoogleQuery(models.Model):
    query_text = models.CharField(max_length=255, blank=True, null=True)
    suggestion = models.CharField(max_length=255, blank=True, null=True)
