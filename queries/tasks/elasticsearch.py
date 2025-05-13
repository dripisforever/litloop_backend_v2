# tasks.py
from celery import shared_task
from .models import Query
from .documents import SuggestionIndex
import requests
from elasticsearch_dsl import Search

@shared_task
def scrape_and_save_autosuggest(query_text):
    # Check if suggestions already exist for the query in Elasticsearch
    s = Search(index='suggestion_index')\
        .filter('term', suggestion=query_text)

    if s.execute():
        return "Suggestions already exist for this query."

    # If no suggestions exist in Elasticsearch, scrape the Autosuggest API and save the results
    api_key = "23c6c54ede484f7c9586245ad7a0fb18"
    url = f"https://api.bing.microsoft.com/v7.0/suggestions?q={query_text}"
    headers = {
        "Ocp-Apim-Subscription-Key": api_key
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if 'suggestionGroups' in data:
        for group in data['suggestionGroups']:
            if 'searchSuggestions' in group:
                for suggestion in group['searchSuggestions']:
                    Query.objects.create(query_text=query_text, suggestion=suggestion['displayText'])
                    # Also index the suggestion in Elasticsearch
                    SuggestionIndex(suggestion=suggestion['displayText']).save()

    return "Scraping and saving completed successfully."
