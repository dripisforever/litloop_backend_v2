# reference: https://github.com/John-Doherty01/docker-celery/blob/3054deb0ccc686eb1afa084ad89a0bcfb12eed83/findmyhitman/hitman_rest_api/views.py#L7
# reference: https://www.youtube.com/watch?v=puy3LdG2nYA
import json
from rest_framework import permissions, status, serializers
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model  # If used custom user model
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from dateutil import parser
from .websocket_serializers import ScheduleJobSerializer, HitJobSerializer, UserSerializer
from .websocket_task import start_new_hit_job

UserModel = get_user_model()


class GetHitmen(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(
            data={"names": ["bill", "bob", "keanu", "logan"]}, status=status.HTTP_200_OK
        )


class StartNewHitJob(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = HitJobSerializer

    def post(self, request):
        name = request.data.get("target_name")
        new_celery_task = start_new_hit_job.delay(name)
        return Response(
            data={
                "result": f"Job created for {name}",
                "celery_task_id": new_celery_task.id,
            },
            status=status.HTTP_200_OK,
        )


class ScheduleNewHitJob(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ScheduleJobSerializer

    def post(self, request):
        name = request.data.get("target_name")
        schedule_time = parser.parse(request.data.get("schedule_time"))
        schedule, _ = CrontabSchedule.objects.get_or_create(
            day_of_week=",".join(request.data.get("days_of_week")),
            minute=schedule_time.minute,
            hour=schedule_time.hour,
        )

        new_celery_task = PeriodicTask.objects.update_or_create(
            name=f"Schedule hit job for {name}",
            defaults={
                "task": "hitman_rest_api.tasks.start_new_hit_job",
                "args": json.dumps([name]),
                "crontab": schedule,
            },
        )

        return Response(
            data={"result": f"Task scheduled for execution"}, status=status.HTTP_200_OK,
        )


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
