import json, os
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from todos.models import Todo
from users.auth_utils import jwt_required_testable

# Get all todos for the current user, optionally filtered by list_id
@csrf_exempt
@jwt_required_testable
def get_todos(request):
    user = request.user
    qs = Todo.objects.filter(user=user)
    list_id = request.GET.get("list_id")
    if list_id:
        qs = qs.filter(todo_list_id=list_id)
    todos = [todo.to_dict() for todo in qs]

    background_image_url = None
    if hasattr(user, 'profile') and user.profile.background_image:
        background_image_url = user.profile.background_image

    return JsonResponse({
        'todos': todos,
        'background_image_url': background_image_url,
    }, safe=False)

# Get single todo
@csrf_exempt
@jwt_required_testable
def get_todo(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id, user=request.user)
        return JsonResponse(todo.to_dict())
    except Todo.DoesNotExist:
        return JsonResponse({"error": "Todo not found"}, status=404)

# Create a todo
@csrf_exempt
@jwt_required_testable
def create_todo(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            todo = Todo.objects.create(
                title=data.get("title", ""),
                completed=data.get("completed", False),
                user=request.user,
                todo_list_id=data.get("todo_list"),
                order=data.get("order", 0),
            )
            return JsonResponse(todo.to_dict(), status=201)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
    return HttpResponseBadRequest("Invalid method")

# Update a todo
@csrf_exempt
@jwt_required_testable
def update_todo(request, todo_id):
    if request.method == "PUT":
        try:
            todo = Todo.objects.get(id=todo_id, user=request.user)
            data = json.loads(request.body)
            todo.title = data.get("title", todo.title)
            todo.completed = data.get("completed", todo.completed)
            if "todo_list" in data:
                todo.todo_list_id = data["todo_list"]
            if "order" in data:
                todo.order = data["order"]
            todo.save()
            return JsonResponse(todo.to_dict())
        except Todo.DoesNotExist:
            return JsonResponse({"error": "Todo not found"}, status=404)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
    return HttpResponseBadRequest("Invalid method")

# Delete a todo
@csrf_exempt
@jwt_required_testable
def delete_todo(request, todo_id):
    if request.method == "DELETE":
        try:
            todo = Todo.objects.get(id=todo_id, user=request.user)
            todo.delete()
            return JsonResponse({"message": "Todo deleted"})
        except Todo.DoesNotExist:
            return JsonResponse({"error": "Todo not found"}, status=404)
    return HttpResponseBadRequest("Invalid method")


@csrf_exempt
@jwt_required_testable
def reorder_todos(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")
    try:
        data = json.loads(request.body)
        items = data.get("items", [])
        for item in items:
            Todo.objects.filter(id=item["id"], user=request.user).update(order=item["order"])
        return JsonResponse({"message": "Reordered"})
    except (json.JSONDecodeError, KeyError) as e:
        return JsonResponse({"error": str(e)}, status=400)
