from django.http import JsonResponse
from videos.spot.tasks_spot import launch_spot_instances_v1
from videos.spot.tasks_main import launch_spot_instances_v2

def launch_spot(request):
    # Call the Celery task asynchronously
    launch_spot_instances.apply_async()

    return JsonResponse({"status": "Spot instances launch request is processing."})
