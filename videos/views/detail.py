from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from videos.models import Video
from litloop_project.r2_storage import r2_url


@csrf_exempt
def video_detail_api(request, video_id):
    try:
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        return JsonResponse({'error': 'Video not found'}, status=404)

    url = r2_url(video.r2_key) or r2_url(video.gcs_key) or r2_url(video.s3_key)
    thumb = video.thumbnail

    data = {
        'id': video.id,
        'pk': video.pk,
        'video_id': video.id,
        'r2_url': url,
        'gcs_url': url,
        'url': url,
        'file': url,
        'file_path': video.r2_key or video.gcs_key or video.s3_key,
        'title': video.title or f'Video {video.id}',
        'name': video.title or f'Video {video.id}',
        'description': video.description or '',
        'thumbnail': thumb,
        'thumbNail': thumb,
        'views_count': video.views,
        'likes_count': video.likes,
        'dislikes_count': video.dislikes,
        'impressions_count': video.impressions,
        'status': video.status,
        'visibility': video.visibility,
        'filename': video.filename,
        'user_id': video.user_id,
    }

    return JsonResponse(data)
