# ref https://gemini.google.com/app/efd78282a573736b
import requests

def call_api(url):
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raises exception for non-2xx status codes
    # Process successful response
  except requests.exceptions.HTTPError as err:
    if err.response.status_code == 429:
      # Handle rate limit here
      print("Rate limit reached for", url)
      # Switch to other endpoint logic
      return switch_to_alternative(url)
    else:
      raise  # Re-raise other exceptions

# Function for alternative endpoint logic
def switch_to_alternative(original_url):
  # Implement logic to choose and call the alternative endpoint here
  # This might involve a different URL or modifying parameters
  alternative_url = "https://api.example.com/alternative"  # Placeholder
  alternative_response = requests.get(alternative_url)
  return alternative_response
