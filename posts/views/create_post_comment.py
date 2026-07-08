import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from posts.models import Post, PostComment
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
def create_post_comment(request, post_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

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

    PostComment.objects.create(
        comment=comment,
        post=post,
    )

    return JsonResponse(serialize_comment(comment), status=201)
