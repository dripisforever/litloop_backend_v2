
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, Http404
from posts.models import Post, PostPhoto
from photos.models import Photo
from users.auth_utils import jwt_required

@csrf_exempt  # since no DRF, you might need this if no CSRF token
@jwt_required
def list_of_posts(request):
    posts = Post.objects.all().order_by('-created_at')

    post_data = []
    for post in posts:
        photos_s3_keys = Photo.objects.filter(postphoto__post=post).values_list('s3_key', flat=True)

        # videos = Video.objects.filter(post=post).values_list('s3_key', flat=True)
        cloudfront_domain = 'https://dgsmmq1mgfewt.cloudfront.net/'
        photos_urls = [cloudfront_domain + key for key in photos_s3_keys]

        post_data.append({
            'id': post.id,
            'title': post.title,
            'description': post.description,
            'author': post.author.username,
            'created_at': post.created_at.isoformat(),
            # 'photos': list(photos),
            'photos': photos_urls,
            # 'videos': list(videos)
        })

    return JsonResponse({'posts': post_data})



def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("Post not found")

    # Get photos linked via PostPhoto relationship
    photos_s3_keys = Photo.objects.filter(postphoto__post=post).values_list('s3_key', flat=True)

    cloudfront_domain = 'https://dgsmmq1mgfewt.cloudfront.net/'
    photos_urls = [cloudfront_domain + key for key in photos_s3_keys]

    data = {
        'id': post.id,
        'title': post.title,
        'description': post.description,
        'author': post.author.username if post.author else None,
        'created_at': post.created_at.isoformat(),
        # 'photos': list(photos),
        'photos': photos_urls,
        # add other fields you want here
    }

    return JsonResponse(data)
