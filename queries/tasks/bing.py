import requests

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from users.models import User
from albums.models import Album

# tasks.py
from celery import shared_task
from .utils import scrape_bing_autosuggest


# for query in response:
#     query_name = query.name
#     Query(name= query_name)


@shared_task
def scrape_and_save_autosuggest(query):
    scrape_bing_autosuggest(query)

    
@shared_task
def bing_task(query, new_value):
    try:
        obj = Query.objects.get(name=query)
        obj.field_to_update = new_value
        obj.save()
    except ObjectDoesNotExist:
        # Handle the case where the object is not found
        pass


    for album_data in feed_info['albums']['items']:
        album_uri = album_data['id']
        album_info = sp.album(album_uri)
        album = Album.create(**album_info)
        # album = await Album.create(**album_info)
        # query_task.delay(**query)
