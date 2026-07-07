import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from videos.models import Video, VideoComment
from comments.models import Comment
from users.auth_utils import jwt_required


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
@jwt_required
def video_comments(request, video_id):
    try:
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        return JsonResponse({'error': 'Video not found'}, status=404)

    if request.method == 'GET':
        comment_ids = VideoComment.objects.filter(video=video).values_list('comment_id', flat=True)
        comments = Comment.objects.filter(id__in=comment_ids).select_related('user').order_by('add_date')
        return JsonResponse({
            'comments': [serialize_comment(c) for c in comments],
        })

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        text = (data.get('text') or '').strip()
        if not text:
            return JsonResponse({'error': 'text is required'}, status=400)

        parent = None
        parent_id = data.get('parent_comment_id')
        if parent_id:
            try:
                parent = Comment.objects.get(id=parent_id)
            except Comment.DoesNotExist:
                return JsonResponse({'error': 'Parent comment not found'}, status=404)

        comment = Comment.objects.create(
            user=request.user,
            text=text,
            parent=parent,
        )

        VideoComment.objects.create(
            comment=comment,
            video=video,
        )

        return JsonResponse(serialize_comment(comment), status=201)

    return JsonResponse({'error': f'Method {request.method} not allowed'}, status=405)
