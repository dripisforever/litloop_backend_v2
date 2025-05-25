# https://chatgpt.com/c/6832c06f-3110-800c-bd4d-a84a93eb9fc6
@api_view(['POST'])
def create_post_with_video(request):
    title = request.data.get('title')
    video_id = request.data.get('video_id')

    if not title or not video_id:
        return Response({"error": "Missing title or video_id"}, status=400)

    try:
        video = Video.objects.get(id=video_id, status='draft')
    except Video.DoesNotExist:
        return Response({"error": "Invalid or already used video"}, status=404)

    post = Post.objects.create(title=title)
    PostVideo.objects.create(post=post, video=video)

    video.status = 'attached'
    video.save(update_fields=['status'])

    return Response({
        "post_id": post.id,
        "title": post.title,
        "video_id": video.id,
        "video_url": video.url
    }, status=201)
