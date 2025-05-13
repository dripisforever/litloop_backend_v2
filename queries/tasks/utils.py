# utils.py
import requests
from .models import BraveQuery
from .documents import SuggestionIndex
from elasticsearch_dsl import Search

def scrape_brave_autosuggest(query):
    api_key = ""
    url = f"https://api.search.brave.com/res/v1/suggest/search?count=20&q={query}"



    # headers = {
    #     "Ocp-Apim-Subscription-Key": api_key
    # }

    s = Search(index='suggestion_index').filter('term', suggestion=query)
    if s.execute():
        return "Suggestions already exist for this query."

    response = requests.get(url, headers=headers)
    data = response.json()

    if 'results' in data:
        for query_term in data['results']:
            if 'query' in query_term:
                for suggestion in query_term['searchSuggestions']:
                    BraveQuery.objects.create(query_text=query, name=suggestion['displayText'])

                    SuggestionIndex(suggestion=suggestion['displayText']).save()

def scrape_bing_autosuggest(query):
    api_key = "23c6c54ede484f7c9586245ad7a0fb18"
    url = f"https://api.bing.microsoft.com/v7.0/suggestions?q={query}"
    headers = {
        "Ocp-Apim-Subscription-Key": api_key
    }

    s = Search(index='suggestion_index').filter('term', suggestion=query)
    if s.execute():
        return "Suggestions already exist for this query."

    response = requests.get(url, headers=headers)
    data = response.json()

    if 'suggestionGroups' in data:
        for group in data['suggestionGroups']:
            if 'searchSuggestions' in group:
                for suggestion in group['searchSuggestions']:
                    Query.objects.create(query_text=query, name=suggestion['displayText'])

                    SuggestionIndex(suggestion=suggestion['displayText']).save()
