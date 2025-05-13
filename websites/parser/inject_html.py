# reference: https://chatgpt.com/g/g-CfL5dQPbs-code-generator/c/824cd638-f5a8-4dc9-8478-df9f5b8f096a

from django.http import HttpResponse, JsonResponse
from django.views import View
import requests
from bs4 import BeautifulSoup

class ModifyHTMLView(View):
    def get(self, request):
        # Get URL from query parameter
        url = request.GET.get('url')
        if not url:
            return JsonResponse({'error': 'URL parameter is required'}, status=400)

        # Fetch HTML content from the URL
        try:
            # headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
            # headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}


            response = requests.get(url, headers=headers)

            response.raise_for_status()  # Raise an exception for HTTP errors
        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

        # Parse the HTML content
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Add script tag
        script_tag = soup.new_tag('script', src='./ANNOTATION_SCRIPT.js')
        if soup.head:
            soup.head.append(script_tag)
        else:
            soup.insert(0, script_tag)

        # Add custom HTML block to the body
        custom_block = '<div>Custom HTML Block Content</div>'
        custom_block_tag = BeautifulSoup(custom_block, 'html.parser')
        if soup.body:
            soup.body.append(custom_block_tag)
        else:
            soup.append(custom_block_tag)

        # Return modified HTML
        modified_html = str(soup)
        return HttpResponse(modified_html, content_type='text/html')
