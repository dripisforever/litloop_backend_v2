import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from todos.models import TodoList
from users.auth_utils import jwt_required_testable


@csrf_exempt
@jwt_required_testable
def get_lists(request):
    lists = TodoList.objects.filter(user=request.user)
    data = [lst.to_dict() for lst in lists]
    return JsonResponse(data, safe=False)


@csrf_exempt
@jwt_required_testable
def create_list(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")
    try:
        data = json.loads(request.body)
        name = data.get("name", "").strip()
        if not name:
            return JsonResponse({"error": "Name is required"}, status=400)
        lst = TodoList.objects.create(name=name, user=request.user, order=data.get("order", 0))
        return JsonResponse(lst.to_dict(), status=201)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")


@csrf_exempt
@jwt_required_testable
def update_list(request, list_id):
    if request.method != "PUT":
        return HttpResponseBadRequest("Invalid method")
    try:
        lst = TodoList.objects.get(id=list_id, user=request.user)
        data = json.loads(request.body)
        name = data.get("name", "").strip()
        if name:
            lst.name = name
        if "order" in data:
            lst.order = data["order"]
        lst.save()
        return JsonResponse(lst.to_dict())
    except TodoList.DoesNotExist:
        return JsonResponse({"error": "List not found"}, status=404)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")


@csrf_exempt
@jwt_required_testable
def delete_list(request, list_id):
    if request.method != "DELETE":
        return HttpResponseBadRequest("Invalid method")
    try:
        lst = TodoList.objects.get(id=list_id, user=request.user)
        lst.delete()
        return JsonResponse({"message": "List deleted"})
    except TodoList.DoesNotExist:
        return JsonResponse({"error": "List not found"}, status=404)


@csrf_exempt
@jwt_required_testable
def reorder_lists(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")
    try:
        data = json.loads(request.body)
        items = data.get("items", [])
        for item in items:
            TodoList.objects.filter(id=item["id"], user=request.user).update(order=item["order"])
        return JsonResponse({"message": "Reordered"})
    except (json.JSONDecodeError, KeyError) as e:
        return JsonResponse({"error": str(e)}, status=400)
