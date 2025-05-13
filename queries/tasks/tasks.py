# tasks.py
from celery import shared_task
from .models import Query
import requests
from .utils import scrape_bing_autosuggest


@shared_task
def scrape_and_save_autosuggest(query_text):
    scrape_bing_autosuggest(query_text)


    if 'suggestionGroups' in data:
        for group in data['suggestionGroups']:
            if 'searchSuggestions' in group:
                for suggestion in group['searchSuggestions']:
                    Query.objects.create(query_text=query_text, suggestion=suggestion['displayText'])
