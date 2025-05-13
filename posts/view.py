from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from posts.models import Post, PostLike
from posts.tasks.increment import process_post_like


class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        """Handle like/unlike"""
        user_id = request.user.id
        process_post_like.delay(user_id, post_id)  # Run task asynchronously
        return Response({'message': 'Like request is being processed'}, status=202)


class PostLikersView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to see likers

    def get(self, request, post_id):
        """Return a list of users who liked a post"""
        likers = PostLike.objects.filter(post_id=post_id).select_related('user')
        liker_data = [{"id": liker.user.id, "username": liker.user.username} for liker in likers]
        return Response({'likers': liker_data})
