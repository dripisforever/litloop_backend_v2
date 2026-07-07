from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from videos.models import Video, VideoComment
from comments.models import Comment
from users.auth_utils import jwt_optional


def serialize_comment(comment):
    return {
        'id': comment.id,
        'text': comment.text,
        'user_id': comment.user_id,
        'username': comment.user.username,
        'avatar': comment.user.avatar,
        'parent_id': comment.parent_id,
        'created_at': comment.add_date.isoformat() if comment.add_date else None,
    }


@csrf_exempt
@jwt_optional
def list_video_comments(request, video_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET allowed'}, status=405)

    try:
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        return JsonResponse({'error': 'Video not found'}, status=404)

    comment_ids = VideoComment.objects.filter(video=video).values_list('comment_id', flat=True)
    comments = Comment.objects.filter(id__in=comment_ids).select_related('user').order_by('add_date')

    return JsonResponse({
        'comments': [serialize_comment(c) for c in comments],
    })
