import json
import requests
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import login
from users.models import User


def exchange_code_for_tokens(code, redirect_uri):
    """Exchange authorization code for access token and id token."""
    payload = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }
    response = requests.post("https://oauth2.googleapis.com/token", data=payload)
    data = response.json()
    if response.status_code != 200 or "error" in data:
        raise ValueError(f"Failed token exchange: {data.get('error_description', data)}")
    return data  # contains access_token, id_token, etc.


def fetch_google_user_info(access_token):
    """Fetch user profile info from Google using access token."""
    response = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", headers={
        "Authorization": f"Bearer {access_token}"
    })
    if response.status_code != 200:
        raise ValueError("Failed to fetch user info from Google")
    return response.json()


def get_or_create_user_from_google_data(google_data):
    """Get or create User from Google profile info."""
    email = google_data.get("email")
    if not email:
        raise ValueError("Email not found in Google user info")
    name = google_data.get("name", "")
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "username": email,  # or generate unique username if needed
            "first_name": name.split()[0] if name else "",
            "last_name": " ".join(name.split()[1:]) if name and len(name.split()) > 1 else "",
        }
    )
    return user, created


@csrf_exempt
def google_token_exchange_view(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST allowed")

    try:
        data = json.loads(request.body)
        code = data.get("code")
        redirect_uri = data.get("redirect_uri") or request.build_absolute_uri("/google/callback")
        if not code:
            return HttpResponseBadRequest("Missing authorization code")
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    try:
        token_data = exchange_code_for_tokens(code, redirect_uri)
        access_token = token_data["access_token"]
        google_user_info = fetch_google_user_info(access_token)
        user, created = get_or_create_user_from_google_data(google_user_info)
        login(request, user)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({
        "message": "User logged in with Google",
        "created": created,
        "username": user.username,
        "email": user.email,
    })
