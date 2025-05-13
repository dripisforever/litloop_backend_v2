# reference: https://www.youtube.com/watch?v=TddYMNVV14g
import requests

# API_KEY = open('API_KEY').read() # https://console.cloud.google.com/apis/credentials?project=customsearchtinkering
# SEARCH_ENGINE_ID = open('SEARCH_ENGINE_ID').read()

API_KEY = 'AIzaSyDmozzxUMPfhu1Tg0yNbAGpuV-ooqpUX0Y'
SEARCH_ENGINE_ID = 'a6c0b28d85a34430d'

search_query = 'Neural Nine books'
url = 'https://www.googleapis.com/customsearch/v1'
params = {
    'q': search_query,
    'key': API_KEY,
    'cx': SEARCH_ENGINE_ID
}

response = requests.get(url, params=params)

results = response.json()

# if 'items' in results:
print(results['items'][0])
# print(results)
