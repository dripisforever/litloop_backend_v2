from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post

class PostCreateViewV2(APIView):
    def post(self, request):
        title = request.data.get('title')  # Handles JSON properly
        if not title:
            return Response({'error': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)

        post = Post.objects.create(title=title)
        return Response({'id': post.id, 'title': post.title}, status=status.HTTP_201_CREATED)
