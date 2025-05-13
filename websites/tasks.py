import requests

# url = 'https://api.search.brave.com/res/v1/suggest/search'
url = 'https://api.search.brave.com/res/v1/web/search'
query = 'a'

params = {'q': query, 'count': '20'}
headers = {
    'x-subscription-token': 'BSA-7IOG54pS0Xwmc8hw5_L07-Cja3_',
    'accept': 'application/json',
    'Accept-Encoding': 'gzip',
    'Cache-Control': 'no-cache'
}

requests.get(url, headers=headers, params=params)
