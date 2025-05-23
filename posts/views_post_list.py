
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from posts.models import Post, PostPhoto
from photos.models import Photo
from users.auth_utils import jwt_required

@csrf_exempt  # since no DRF, you might need this if no CSRF token
@jwt_required
def list_of_posts(request):
    posts = Post.objects.all().order_by('-created_at')

    post_data = []
    for post in posts:
        photos = Photo.objects.filter(post=post).values_list('s3_key', flat=True)
        # videos = Video.objects.filter(post=post).values_list('s3_key', flat=True)

        post_data.append({
            'id': post.id,
            'title': post.title,
            'description': post.description,
            'author': post.author.username,
            'created_at': post.created_at.isoformat(),
            'photos': list(photos),
            # 'videos': list(videos)
        })

    return JsonResponse({'posts': post_data})
