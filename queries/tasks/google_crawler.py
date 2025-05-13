# utils.py
import requests
from .models import Query
from .documents import SuggestionIndex
from elasticsearch_dsl import Search

def scrape_bing_autosuggest(query):
    url = f"https://google.com/complete/search"
    params = {
        'q': query,
        'client': 'firefox',

    }

    s = Search(index='suggestion_index').filter('term', suggestion=query)
    if s.execute():
        return "Suggestions already exist for this query."

    response = requests.get(url, headers=headers)
    data = response.json()

    data[1]

    output = {
        "results": [{"query": item} for item in data[1]]
    }

    Query.objects.create(query_text=query, name=suggestion['displayText'])

    SuggestionIndex(suggestion=suggestion['displayText']).save()
