# ref https://chatgpt.com/c/548a7e67-39d0-48bc-b6c3-6d54a72a8844
import requests
import time

def call_api_with_retry(url, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limit exceeded
                # Implement exponential backoff
                wait_time = 2 ** retries
                print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                retries += 1
            else:
                # Handle other status codes if needed
                print(f"Unexpected status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    print("Max retries exceeded. Unable to fetch data.")
    return None

# Example usage
api_url = "https://api.example.com/data"
data = call_api_with_retry(api_url)
if data:
    # Process the data
    print(data)
else:
    print("Failed to fetch data.")
