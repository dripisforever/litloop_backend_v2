from celery import shared_task

from memes.models import Meme


@shared_task
def save_memes(raw_memes):
    for item in raw_memes:
        Meme.objects.get_or_create(
            meme_id=item.get('postLink', str(item.get('title', ''))),
            defaults={
                'title': item.get('title', ''),
                'url': item.get('url', ''),
                'post_link': item.get('postLink', ''),
                'subreddit': item.get('subreddit', ''),
                'author': item.get('author', ''),
                'nsfw': item.get('nsfw', False),
                'spoiler': item.get('spoiler', False),
                'ups': item.get('ups', 0),
                'preview': item.get('preview', ''),
            }
        )
