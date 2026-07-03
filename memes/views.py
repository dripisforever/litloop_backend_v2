import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from memes.models import Meme
from memes.subreddits import SUBREDDITS
from memes.tasks import save_memes


MEMES_TOTAL = 26


def memes_list_view(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    count_per_sub = max(1, MEMES_TOTAL // len(SUBREDDITS))
    extra = MEMES_TOTAL - count_per_sub * len(SUBREDDITS)

    raw_memes = []

    for i, sub in enumerate(SUBREDDITS):
        c = count_per_sub + (1 if i < extra else 0)
        try:
            resp = requests.get(f'https://meme-api.com/gimme/{sub}/{c}', timeout=10)
            resp.raise_for_status()
            data = resp.json()
            raw_memes.extend(data.get('memes', []))
        except requests.RequestException:
            continue

    save_memes.delay(raw_memes)

    memes_data = [{
        'id': None,
        'title': item.get('title', ''),
        'url': item.get('url', ''),
        'post_link': item.get('postLink', ''),
        'subreddit': item.get('subreddit', ''),
        'author': item.get('author', ''),
        'nsfw': item.get('nsfw', False),
        'ups': item.get('ups', 0),
        'preview': item.get('preview', ''),
    } for item in raw_memes]

    return JsonResponse(memes_data, safe=False)


def memes_list_db_view(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    memes = Meme.objects.all().order_by('-created_at')[:50]
    data = [{
        'id': m.id,
        'title': m.title,
        'url': m.url,
        'post_link': m.post_link,
        'subreddit': m.subreddit,
        'author': m.author,
        'nsfw': m.nsfw,
        'ups': m.ups,
        'preview': m.preview,
        'likes': m.liked_by.count(),
    } for m in memes]
    return JsonResponse(data, safe=False)
