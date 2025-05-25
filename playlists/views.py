from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from django.core.paginator import Paginator
from django.forms.models import model_to_dict

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

from .models import Playlist
from django.contrib.auth.models import User  # Assuming user field is a FK to auth.User

SPOTIPY_CLIENT_ID = "0575ef8642c94277b3fec71f400ee600"
SPOTIPY_CLIENT_SECRET = "21c16d49607b49cd8bbe4a5897c63de4"

sp = Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET
    )
)


def playlist_detail(request, playlist_uri):
    if request.method != "GET":
        return HttpResponseBadRequest("Only GET is allowed")
    results = sp.playlist(playlist_uri)
    return JsonResponse(results)


def playlist_offset(request, playlist_uri):
    if request.method != "GET":
        return HttpResponseBadRequest("Only GET is allowed")

    offset = request.GET.get('offset', 0)
    limit = request.GET.get('limit', 100)

    try:
        offset = int(offset)
        limit = int(limit)
    except ValueError:
        return HttpResponseBadRequest("Offset and limit must be integers")

    results = sp.playlist_tracks(playlist_uri, offset=offset, limit=limit)
    return JsonResponse(results)


class PlaylistListView(View):
    def get(self, request):
        playlists = Playlist.objects.select_related("user").all()

        author = request.GET.get("author")
        if author:
            playlists = playlists.filter(user__username=author)

        paginator = Paginator(playlists, 10)
        page_number = request.GET.get("page", 1)
        page = paginator.get_page(page_number)

        data = [
            {
                "id": playlist.id,
                "name": playlist.name,
                "user": playlist.user.username,
                "description": playlist.description,
                # Add more fields as needed
            }
            for playlist in page
        ]

        return JsonResponse({
            "count": paginator.count,
            "num_pages": paginator.num_pages,
            "current_page": page.number,
            "results": data,
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        name = body.get('name')
        description = body.get('description', '')

        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)

        playlist = Playlist.objects.create(
            name=name,
            description=description,
            user=request.user,
        )

        return JsonResponse({
            "id": playlist.id,
            "name": playlist.name,
            "description": playlist.description,
            "user": playlist.user.username
        }, status=201)
