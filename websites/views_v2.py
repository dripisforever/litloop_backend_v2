import requests
from django.http import JsonResponse
from django.views import View


class BingWebsiteSearchView(View):
    def get(self, request, *args, **kwargs):
        query_text = request.GET.get('q')
        api_key = "bef3f98862ac4222806c3bfd0ffa9bb6"
        url = f"https://api.bing.microsoft.com/v7.0/search?q={query_text}&cc=en-US&setLang=en&mkt=en-US&count=40"
        headers = {
            "Ocp-Apim-Subscription-Key": api_key
        }

        response = requests.get(url, headers=headers)
        data = response.json()
        results = data.get('webPages', {}).get('value', [])
        return JsonResponse({'results': results})


class BingImageSearchView(View):
    def get(self, request, *args, **kwargs):
        query_text = request.GET.get('q')
        api_key = "bef3f98862ac4222806c3bfd0ffa9bb6"
        url = f"https://api.bing.microsoft.com/v7.0/images/search?q={query_text}&safeSearch=Off"
        headers = {
            "Ocp-Apim-Subscription-Key": api_key
        }

        response = requests.get(url, headers=headers)
        data = response.json()
        results = data.get('value', [])
        return JsonResponse({'results': results})


class BraveWebsiteSearchView(View):
    def get(self, request, *args, **kwargs):
        query_text = request.GET.get('q')

        if "site:" in query_text:
            api_key = "bef3f98862ac4222806c3bfd0ffa9bb6"
            url = f"https://api.bing.microsoft.com/v7.0/search?q={query_text}&cc=en-US&setLang=en&mkt=en-US&count=40"
            headers = {
                "Ocp-Apim-Subscription-Key": api_key
            }

            response = requests.get(url, headers=headers)
            data = response.json()
            results = data.get('webPages', {}).get('value', [])
            return JsonResponse({'results': results})

        api_key = "BSA-7IOG54pS0Xwmc8hw5_L07-Cja3_"
        url = f"https://api.search.brave.com/res/v1/web/search?q={query_text}"
        headers = {
            "x-subscription-token": api_key,
            'accept': 'application/json',
            'Cache-Control': 'no-cache',
            'Accept-Encoding': 'gzip'
        }

        response = requests.get(url, headers=headers)
        data = response.json()
        results = data.get('web', {}).get('results', [])
        return JsonResponse({'results': results})


class BraveImageSearchView(View):
    def get(self, request, *args, **kwargs):
        query_text = request.GET.get('q')
        api_key = "BSA-7IOG54pS0Xwmc8hw5_L07-Cja3_"
        url = "https://api.search.brave.com/res/v1/images/search"
        headers = {
            "x-subscription-token": api_key,
            'accept': 'application/json',
            'Cache-Control': 'no-cache',
            'Accept-Encoding': 'gzip'
        }

        params = {
            'q': query_text,
            'safesearch': 'off',
        }

        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        return JsonResponse(data)


class GoogleCustomSearchImageView(View):
    def get(self, request, *args, **kwargs):
        query_text = request.GET.get('q')
        API_KEY = 'AIzaSyDmozzxUMPfhu1Tg0yNbAGpuV-ooqpUX0Y'
        SEARCH_ENGINE_ID = 'a6c0b28d85a34430d'

        url = 'https://www.googleapis.com/customsearch/v1'
        params = {
            'q': query_text,
            'key': API_KEY,
            'cx': SEARCH_ENGINE_ID,
            'searchType': 'image',
        }

        response = requests.get(url, params=params)
        results = response.json()
        return JsonResponse({'items': results.get('items', [])})
