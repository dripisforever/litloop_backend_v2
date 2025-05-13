import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from users.models import User
from users.jwt_auth import generate_jwt

@csrf_exempt
def signup_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    data     = json.loads(request.body)
    username = data.get('username')
    email    = data.get('email')
    password = data.get('password')

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    token = generate_jwt(user)
    return JsonResponse({'token': token})

@csrf_exempt
def signin_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')

    user = authenticate(email=email, password=password)
    if not user:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

    token = generate_jwt(user)
    return JsonResponse({'token': token})
