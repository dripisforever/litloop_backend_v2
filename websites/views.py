import requests
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
# class WebsiteCreateView(generics.CreateAPIView):
class BingWebsiteSearchView(APIView):
    # serializer_class = WebsiteSerializer

    def get(self, request, *args, **kwargs):
        # query_text = request.data.get('q', '')
        query_text = self.request.query_params.get('q', None)
        # scrape_and_save_autosuggest.delay(query_text)  # Trigger the Celery task asynchronously

        # response_filter = 'RelatedSearches,WebPages,Images,Videos'
        # response_filter = 'Videos'
        # response_filter = 'Images'
        # api_key = "23c6c54ede484f7c9586245ad7a0fb18"
        api_key = "bef3f98862ac4222806c3bfd0ffa9bb6"
        # url = f"https://api.bing.microsoft.com/v7.0/search?responseFilter={response_filter}&q={query_text}&cc=en-US&setLang=en&mkt=en-US&count=10"
        url = f"https://api.bing.microsoft.com/v7.0/search?q={query_text}&cc=en-US&setLang=en&mkt=en-US&count=40"
        headers = {
            "Ocp-Apim-Subscription-Key": api_key
        }


        response = requests.get(url, headers=headers)
        data = response.json()
        results = data['webPages']['value']
        return Response({'results': results })
        # return Response({'results': data })
        # return Response(data)


class BingImageSearchView(APIView):
    # serializer_class = WebsiteSerializer

    def get(self, request, *args, **kwargs):
        # query_text = request.data.get('q', '')
        query_text = self.request.query_params.get('q', None)
        # scrape_and_save_autosuggest.delay(query_text)  # Trigger the Celery task asynchronously

        # response_filter = 'RelatedSearches,WebPages,Images,Videos'
        # response_filter = 'Videos'
        # response_filter = 'Images'
        api_key = "bef3f98862ac4222806c3bfd0ffa9bb6"
        # url = f"https://api.bing.microsoft.com/v7.0/search?responseFilter={response_filter}&q={query_text}&cc=en-US&setLang=en&mkt=en-US&count=10"
        url = f"https://api.bing.microsoft.com/v7.0/images/search?q={query_text}&safeSearch=Off"
        headers = {
            "Ocp-Apim-Subscription-Key": api_key
        }

        # from time import sleep
        # sleep(2)

        response = requests.get(url, headers=headers)
        data = response.json()
        results = data['value']
        return Response({'results': results })
        # return Response(data)


class BraveWebsiteSearchView(APIView):
    # serializer_class = WebsiteSerializer

    def get(self, request, *args, **kwargs):
        # query_text = request.data.get('q', '')
        # query_text = self.request.query_params.get('q', None)
        query_text = request.GET.get('q')
        # scrape_and_save_autosuggest.delay(query_text)  # Trigger the Celery task asynchronously
        api_key = "BSA-7IOG54pS0Xwmc8hw5_L07-Cja3_"
        url = f"https://api.search.brave.com/res/v1/web/search?q={query_text}"
        headers = {
            "x-subscription-token": api_key,
            'accept': 'application/json',
            'Cache-Control': 'no-cache',
            'Accept-Encoding': 'gzip'
        }


        if "site:" in query_text:
            api_key = "bef3f98862ac4222806c3bfd0ffa9bb6"
            # url = f"https://api.bing.microsoft.com/v7.0/search?responseFilter={response_filter}&q={query_text}&cc=en-US&setLang=en&mkt=en-US&count=10"
            url = f"https://api.bing.microsoft.com/v7.0/search?q={query_text}&cc=en-US&setLang=en&mkt=en-US&count=40"
            headers = {
                "Ocp-Apim-Subscription-Key": api_key
            }


            response = requests.get(url, headers=headers)
            data = response.json()
            results = data['webPages']['value']
            return Response({'results': results })

        response = requests.get(url, headers=headers)
        data = response.json()

        # return Response({'message': 'Scraping initiated. Results will be saved shortly.'})
        results = data['web']['results']
        return Response({'results': results })
        # return Response(data)


class BraveImageSearchView(APIView):
    # serializer_class = WebsiteSerializer

    def get(self, request, *args, **kwargs):
        # query_text = request.data.get('q', '')
        # query_text = self.request.query_params.get('q', None)
        query_text = request.GET.get('q')
        # scrape_and_save_autosuggest.delay(query_text)  # Trigger the Celery task asynchronously
        api_key = "BSA-7IOG54pS0Xwmc8hw5_L07-Cja3_"
        url = f"https://api.search.brave.com/res/v1/images/search"
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

        # return Response({'message': 'Scraping initiated. Results will be saved shortly.'})
        # results = data['results']
        # return Response({'results': results })
        return Response(data)


class GoogleCustomSearchImageView(APIView):
    # serializer_class = WebsiteSerializer

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
            # 'lr': 'lang_en',
            # 'gl': 'UK',
        }

        response = requests.get(url, params=params)


        results = response.json()
        return Response({ 'items': results['items'] })

        # results = response.json()['items']
        # return Response(results)
