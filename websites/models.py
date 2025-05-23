from django.db import models

# Create your models here.
class Website(models.Model):
    url   = models.URLField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    body  = models.TextField(blank=True, null=True)

    favicon    = models.CharField(max_length=400, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# class WebsiteLike(models.Model):
#     website = models.ForeignKey()
#     user = models.ForeignKey()
#     query_text = models.ForeignKey()
