# search_indexes.py
from elasticsearch_dsl import Document, Text

class SuggestionIndex(Document):
    suggestion = Text()

    class Index:
        name = 'suggestion_index'
