from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import HttpResponse

from posts.models import Post
from users.models import User

from views.tasks import process_view

class ViewsUP(APIView):
    def post(self, request):

        user_id = request.POST['user_id']
        post_id = request.POST['post_id']
        result = process_view.delay(user_id, post_id)

        # return Response(status=status.HTTP_202_ACCEPTED)
        return HttpResponse(f'View Accepted {result.id}')
