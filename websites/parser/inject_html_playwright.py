from django.http import HttpResponse, JsonResponse
from django.views import View
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ModifyHTMLView(View):
    def get(self, request):
        # Get URL from query parameter
        url = request.GET.get('url')
        if not url:
            return JsonResponse({'error': 'URL parameter is required'}, status=400)

        # Set up Selenium WebDriver
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            # Open the URL
            driver.get(url)

            # Wait for the page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )

            # Inject the script tag
            script = driver.execute_script("""
                var script = document.createElement('script');
                script.src = './ANNOTATION_SCRIPT.js';
                document.head.appendChild(script);
            """)

            # Inject the custom HTML block into the body
            custom_block = """
                var div = document.createElement('div');
                div.innerHTML = 'Custom HTML Block Content';
                document.body.appendChild(div);
            """
            driver.execute_script(custom_block)

            # Get the modified HTML
            modified_html = driver.page_source

            # Close the WebDriver
            driver.quit()

            return HttpResponse(modified_html, content_type='text/html')

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
