

api_key = "23c6c54ede484f7c9586245ad7a0fb18"
# url = f"https://api.bing.microsoft.com/v7.0/search?responseFilter={response_filter}&q={query_text}&cc=en-US&setLang=en&mkt=en-US&count=10"
url = f"https://api.bing.microsoft.com/v7.0/search?q={query_text}&cc=en-US&setLang=en&mkt=en-US&count=10"
headers = {
    "Ocp-Apim-Subscription-Key": api_key
}


response = requests.get(url, headers=headers)
data = response.json()
