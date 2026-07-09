from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from posts.models import Post, PostComment
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
def detail_post_comment(request, post_id, comment_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET allowed'}, status=405)

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    if not PostComment.objects.filter(post=post, comment_id=comment_id).exists():
        return JsonResponse({'error': 'Comment not found on this post'}, status=404)

    try:
        comment = Comment.objects.select_related('user').get(id=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comment not found'}, status=404)

    return JsonResponse(serialize_comment(comment))
